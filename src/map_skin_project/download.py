import os
import osmnx as ox

from utils import ensure_path

def download_osm_layers(place_name: str, save_dir: str = "data"):
    """
    根據地名下載 OSM 圖層（建築、公園、道路、水域）並各自儲存為 GeoJSON。

    Args:
        place_name (str): 地名，例如 "Xinyi District, Taipei, Taiwan"
        save_dir (str): 儲存資料夾
    Returns:
        dict: 包含各圖層名稱與對應 GeoDataFrame 的字典
    """
    os.makedirs(save_dir, exist_ok=True)
    layers = {}

    # 建築物
    print("🏢 下載建築物...")
    gdf_building = ox.features.features_from_place(place_name, tags={"building": True})
    gdf_building.to_file(ensure_path(save_dir, "buildings.geojson"), driver="GeoJSON")
    layers["buildings"] = gdf_building

    # 公園
    print("🌳 下載公園...")
    gdf_parks = ox.features.features_from_place(place_name, tags={"leisure": "park"})
    gdf_parks.to_file(ensure_path(save_dir, "parks.geojson"), driver="GeoJSON")
    layers["parks"] = gdf_parks

    # 道路
    print("🛣️ 下載道路...")
    gdf_roads = ox.features.features_from_place(place_name, tags={"highway": True})
    gdf_roads.to_file(ensure_path(save_dir, "roads.geojson"), driver="GeoJSON")
    layers["roads"] = gdf_roads

    # 河流與湖泊
    print("🌊 下載水域與森林...")
    gdf_water = ox.features.features_from_place(place_name, tags={"natural": ["water", "wood"]})
    gdf_water.to_file(ensure_path(save_dir, "water.geojson"), driver="GeoJSON")
    layers["water"] = gdf_water

    print(f"✅ 所有圖層已儲存至：{save_dir}/")
    return layers


# 測試
if __name__ == "__main__":
    download_osm_layers("Xinyi District, Taipei, Taiwan")
