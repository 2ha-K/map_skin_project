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

# utils.py

import matplotlib.image as mpimg
import numpy as np
from shapely.geometry import Polygon, MultiPolygon

def plant_tree_on_forest_layer(ax, gdf, icon_path, count_per_polygon=10, size_range=(30, 60), zorder=100):
    """
    在 forest 的 GeoDataFrame 上隨機種樹。

    Args:
        ax: matplotlib 的座標系（通常是 plt.gca()）
        gdf: forest 的 GeoDataFrame
        icon_path: 樹的圖檔路徑（透明背景 PNG）
        count_per_polygon: 每個多邊形種幾棵
        size_range: 每棵樹的大小區間（單位與座標一致）
        zorder: 畫面堆疊層級
    """
    img = mpimg.imread(icon_path)
    for geom in gdf.geometry:
        if geom is None:
            continue
        polys = [geom] if isinstance(geom, Polygon) else (
            geom.geoms if isinstance(geom, MultiPolygon) else []
        )
        for poly in polys:
            minx, miny, maxx, maxy = poly.bounds
            for _ in range(count_per_polygon):
                for _ in range(10):  # 最多嘗試 10 次找內部點
                    x = np.random.uniform(minx, maxx)
                    y = np.random.uniform(miny, maxy)
                    if poly.contains(poly.representative_point()):
                        size = np.random.uniform(*size_range)
                        ax.imshow(
                            img,
                            extent=[x - size/2, x + size/2, y - size/2, y + size/2],
                            zorder=zorder
                        )
                        break
