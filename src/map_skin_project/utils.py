from pathlib import Path
import re

def ensure_path(directory: str, filename: str) -> Path:
    """
    建立目錄並回傳組合後的完整路徑。

    Args:
        directory (str): 資料夾名稱
        filename (str): 檔案名稱（例如 map.geojson）

    Returns:
        Path: 完整的儲存路徑
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path / filename

def slugify(name: str):
    return re.sub(r'\W+', '_', name.lower()).strip('_')


import matplotlib.image as mpimg
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely import affinity


def plant_trees(ax, gdf_forest, tree_img_path, count_per_polygon=10):
    tree_img = mpimg.imread(tree_img_path)
    for geom in gdf_forest.geometry:
        if geom is None:
            continue
        if isinstance(geom, Polygon):
            polys = [geom]
        elif isinstance(geom, MultiPolygon):
            polys = list(geom.geoms)
        else:
            continue

        for poly in polys:
            minx, miny, maxx, maxy = poly.bounds
            for _ in range(count_per_polygon):
                for _ in range(10):  # 最多嘗試 10 次找在內部的點
                    x = np.random.uniform(minx, maxx)
                    y = np.random.uniform(miny, maxy)
                    point = poly.representative_point().interpolate(0.5, normalized=True)
                    if poly.contains(point):
                        size = np.random.uniform(30, 60)  # 樹圖片大小（像素）
                        ax.imshow(
                            tree_img,
                            extent=[x - size / 2, x + size / 2, y - size / 2, y + size / 2],
                            zorder=100
                        )
                        break
