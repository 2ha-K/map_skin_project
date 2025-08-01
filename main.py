from map_skin_project.download import download_osm_layers
from map_skin_project.render import render_map
from map_skin_project.map_utils import slugify
from map_skin_project.plant_trees import plant_trees_at_random_green

location = "東海大學, 台中市, 台灣"
download_osm_layers(location)

base_output_path = f"output/{slugify(location)}.png"
render_map(
    data_dir="data",  # 你放 geojson 的資料夾
    output_path=base_output_path  # 圖片會出現在 output 資料夾
)

tree_output_path = f"output/{slugify(location)}_with_trees.png"
plant_trees_at_random_green(tree_real_world_size_m=100, trees_num=30, base_path=base_output_path, output_path=tree_output_path, grid_size=300)

print(f"✅ 測試完成！請查看: {tree_output_path}")