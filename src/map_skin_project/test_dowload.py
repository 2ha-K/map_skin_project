from download import download_osm_layers
from  render import render_map

download_osm_layers("清華大學, 新竹市, 台灣")

render_map(
    data_dir="data",  # 你放 geojson 的資料夾
    output_path="output/test_map.png"  # 圖片會出現在 output 資料夾
)

print("✅ 測試完成！請查看 output/test_map.png")