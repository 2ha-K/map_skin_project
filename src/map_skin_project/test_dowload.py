from download import download_osm_layers
from  render import render_map
from PIL import Image

download_osm_layers(place_name="逢甲大學, 台中市, 台灣")
# download_osm_layers(mode="bbox", bbox=(120.6415, 24.1805, 120.6498,24.1858))
# download_osm_layers(mode="longitude_latitude", center_longitude_latitude=(121.5397, 25.0173))

render_map(
    data_dir="data",  # 你放 geojson 的資料夾
    output_path="output/test_map.png"  # 圖片會出現在 output 資料夾
)

image = Image.open("output/test_map.png")
image.show()

print("✅ 測試完成！請查看 output/test_map.png")