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
        "rivers": {"color": "#8c8ced", "alpha": 1.0, "linewidth": 0.3},  # 河流(可能不需要)
        "forest": {"color": "#a1c96a", "alpha": 1.0, "linewidth": 0},  # 加上樹林
        "parks": {"color": "#c4e292", "alpha": 1.0, "linewidth": 0},  # 加上小草
        "roads": {"color": "#ffffff", "alpha": 1.0, "linewidth": 0.5},
        "water": {"color": "#8c8ced", "alpha": 1.0, "linewidth": 0},  # 湖水
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
                    if layer == "roads" and "highway" in gdf.columns:
                        # 設定每種道路類型的寬度
                        highway_width_map = {
                            "motorway": 0.0,#,  # 高速公路：顯著寬，通常雙向4~6線道
                            "trunk": 0.0,#28.0,  # 幹道：略小於高速公路
                            "primary": 0.0,#24.0,  # 主要幹道：一般大馬路
                            "secondary": 0.0,#18.0,  # 次要道路：次要市區道路
                            "tertiary": 0.0,#12.0,  # 第三級道路：街道或巷道
                            "residential": 0.0,#9.0,  # 住宅道路：社區道路
                            "unclassified": 0.0,#8.0,  # 不明類別：常當作一般小路顯示
                            "service": 4.0,#6.0,  # 服務道路：停車場進出道、小巷
                            "living_street": 0.0,#6.0,  # 居住街道：人車共道
                            "pedestrian": 1.0,#5.0,  # 行人道：僅限人行的步道
                            "footway": 0.0,#4.0,  # 腳踏步道：小徑
                            "cycleway": 0.0,#4.0,  # 單車道：城市腳踏車道
                            "path": 0.0,#3.5  # 小路、田野間步道
                        }

                        # 新增一欄 width，根據 highway 值對應
                        gdf["width"] = gdf["highway"].map(highway_width_map).fillna(0.5)

                        # 分類畫出不同線寬的道路
                        for highway_type, group in gdf.groupby("highway"):
                            lw = highway_width_map.get(highway_type, 0.5)
                            group.plot(
                                ax=ax,
                                color=style["color"],
                                alpha=style["alpha"],
                                linewidth=lw
                            )
                    else:
                        # 非道路圖層照舊處理
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
    plt.tight_layout() #  自動調整畫布內的空間配置，避免圖形被截掉
    os.makedirs(os.path.dirname(output_path), exist_ok=True)# exist_ok=True 表示：「如果資料夾已經存在也沒關係，不會報錯」。
    plt.savefig(output_path, dpi=600, bbox_inches='tight', pad_inches=0, facecolor="#d2d2f7", transparent=False)
    """
    bbox_inches='tight'	自動裁切圖片邊緣的空白區域
    pad_inches=0	不保留邊界空間（等於邊到邊）
    """
    plt.close()
