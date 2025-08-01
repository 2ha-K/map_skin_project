# src/render.py

import geopandas as gpd
import matplotlib.pyplot as plt
import os


def render_map(data_dir="data", output_path="output/xinyi_map.png", skin_fn=None):
    """
    TODO: 貼皮功能
    讀取 GeoJSON 並畫出地圖，支援貼皮圖層函數（可選）。

    Args:
        data_dir (str): 存放 geojson 的資料夾路徑
        output_path (str): 最終輸出的 PNG 圖片位置
        skin_fn (function): 可選的自訂貼皮函式，會傳入 plt.gca() 當前畫布
    """
    plt.figure(figsize=(10, 10)) #建立畫布
    ax = plt.gca() # gca = get current axes，取得當前的座標區
    # ax.set_facecolor("#d2d2f7") # 沒設定到顏色的基礎色

    layer_styles = {
        "water": {"color": "#8c8ced", "alpha": 0.6, "linewidth": 0},  # 湖水
        "rivers": {"color": "#8c8ced", "alpha": 0.8, "linewidth": 0.3},  # 河流(可能不需要)
        "parks": {"color": "#c4e292", "alpha": 0.8, "linewidth": 0}, # 加上小草
        "forest": {"color": "#a1c96a", "alpha": 0.6, "linewidth": 0}, #加上樹林
        "roads": {"color": "#ffffff", "alpha": 1.0, "linewidth": 0.5},
        "buildings": {"color": "#c2b7cd", "alpha": 1.0, "linewidth": 0}
    }

    """
    方法	回傳內容	用法範例
    .keys()	所有 key	for k in d.keys()
    .values()	所有值	for v in d.values()
    .items()	所有 (key, value)	✅ for k, v in d.items() ← 你用的這個
    """
    for layer, style in layer_styles.items():
        filepath = os.path.join(data_dir, f"{layer}.geojson")
        if os.path.exists(filepath):
            try:
                gdf = gpd.read_file(filepath)
                if not gdf.empty:
                    gdf.plot(
                        ax=ax,
                        color=style["color"],
                        alpha=style["alpha"], # 使用透明度（0 = 透明，1 = 不透明）
                        linewidth=style["linewidth"] # 線條粗細，適用於線狀圖層（如道路、河流）
                    )
            except Exception as e:
                print(f"⚠️ Failed to render layer: {layer}, error: {e}")

    # 可選的貼皮（如貼圖、特效）
    if skin_fn:
        skin_fn(ax)

    plt.axis('off')
    plt.tight_layout() #  自動調整畫布內的空間配置，避免圖形被截掉
    os.makedirs(os.path.dirname(output_path), exist_ok=True)# exist_ok=True 表示：「如果資料夾已經存在也沒關係，不會報錯」。
    plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0, facecolor="#d2d2f7", transparent=False)
    """
    bbox_inches='tight'	自動裁切圖片邊緣的空白區域
    pad_inches=0	不保留邊界空間（等於邊到邊）
    """
    plt.close()
