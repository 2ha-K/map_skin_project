# src/render.py

import geopandas as gpd
import matplotlib.pyplot as plt
import os


def render_map(data_dir="data", output_path="output/xinyi_map.png", skin_fn=None):
    """
    讀取 GeoJSON 並畫出地圖，支援貼皮圖層函數（可選）。

    Args:
        data_dir (str): 存放 geojson 的資料夾路徑
        output_path (str): 最終輸出的 PNG 圖片位置
        skin_fn (function): 可選的自訂貼皮函式，會傳入 plt.gca() 當前畫布
    """
    plt.figure(figsize=(10, 10))
    ax = plt.gca()

    layer_styles = {
        "water": {"color": "#68a7f5", "alpha": 0.6, "linewidth": 0},  # 湖水
        "rivers": {"color": "#5ca0d3", "alpha": 0.8, "linewidth": 0.3},  # 河流
        "parks": {"color": "#b6e3b2", "alpha": 0.8, "linewidth": 0},
        "forest": {"color": "#a1c96a", "alpha": 0.6, "linewidth": 0},
        "roads": {"color": "#cccccc", "alpha": 1.0, "linewidth": 0.5},
        "buildings": {"color": "#4a4a4a", "alpha": 1.0, "linewidth": 0}
    }

    for layer, style in layer_styles.items():
        filepath = os.path.join(data_dir, f"{layer}.geojson")
        if os.path.exists(filepath):
            try:
                gdf = gpd.read_file(filepath)
                if not gdf.empty:
                    gdf.plot(
                        ax=ax,
                        color=style["color"],
                        alpha=style["alpha"],
                        linewidth=style["linewidth"]
                    )
            except Exception as e:
                print(f"⚠️ Failed to render layer: {layer}, error: {e}")

    # 可選的貼皮（如貼圖、特效）
    if skin_fn:
        skin_fn(ax)

    plt.axis('off')
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0)
    plt.close()
