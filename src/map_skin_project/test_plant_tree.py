# test_plant_tree.py

from render import render_map
import geopandas as gpd
from utils import plant_tree_on_forest_layer

def add_tree_decorator(ax):
    forest_path = "data/forest.geojson"
    if not forest_path:
        print("❌ 找不到 forest.geojson")
        return

    forest_gdf = gpd.read_file(forest_path)
    if forest_gdf.empty:
        print("❌ forest.geojson 是空的")
        return

    icon_path = "assets/tree.png"
    plant_tree_on_forest_layer(ax, forest_gdf, icon_path, count_per_polygon=5)

if __name__ == "__main__":
    print("🌲 正在種樹並輸出地圖...")
    render_map(data_dir="data", output_path="output/test_tree.png", skin_fn=add_tree_decorator)
    print("✅ 渲染完成，請查看 output/test_tree.png")
