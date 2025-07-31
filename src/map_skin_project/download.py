import os
import osmnx as ox

from utils import ensure_path

def download_osm_layers(place_name: str, save_dir: str = "data"):
    """
    TODO: 加強精準度
    https://wiki.openstreetmap.org/wiki/Zh-hant:Map_Features
    根據地名下載 OSM 圖層並各自儲存為 GeoJSON，適用於遊戲地圖製作。

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

    # 公園（leisure=park or playground）
    print("🌳 下載公園與綠地...")
    gdf_parks = ox.features.features_from_place(place_name, tags={
        "leisure": True,
        "landuse": True,
        "natural": ["grassland", "wood"]
    })
    gdf_parks.to_file(ensure_path(save_dir, "parks.geojson"), driver="GeoJSON")
    layers["parks"] = gdf_parks

    # 道路（各級道路）
    road_types = [
        "motorway", "trunk", "primary", "secondary", "tertiary",
        "residential", "unclassified", "service", "living_street",
        "pedestrian", "footway", "cycleway", "path"
    ]
    print("🛣️ 下載道路...")
    gdf_roads = ox.features.features_from_place(place_name, tags={"highway": road_types})
    gdf_roads.to_file(ensure_path(save_dir, "roads.geojson"), driver="GeoJSON")
    layers["roads"] = gdf_roads

    # 河流、湖泊（natural=water or waterway）
    print("🌊 下載水體（水域）...")
    gdf_water = ox.features.features_from_place(place_name, tags={"natural": "water"})
    gdf_water.to_file(ensure_path(save_dir, "water.geojson"), driver="GeoJSON")
    layers["water"] = gdf_water

    # 河川與溪流（流動水體）
    print("🛶 下載河流與溪流...")
    gdf_rivers = ox.features.features_from_place(place_name, tags={"waterway": True})
    gdf_rivers.to_file(ensure_path(save_dir, "rivers.geojson"), driver="GeoJSON")
    layers["rivers"] = gdf_rivers

    # 森林或樹林區（natural=wood）
    print("🌲 下載森林區...")
    gdf_wood = ox.features.features_from_place(place_name, tags={"natural": "wood"})
    gdf_wood.to_file(ensure_path(save_dir, "forest.geojson"), driver="GeoJSON")
    layers["forest"] = gdf_wood

    # 可選：地標（POI）
    # print("📍下載學校與車站...")
    # gdf_poi = ox.features.features_from_place(place_name, tags={"amenity": ["school", "bus_station"]})
    # gdf_poi.to_file(ensure_path(save_dir, "poi.geojson"), driver="GeoJSON")
    # layers["poi"] = gdf_poi

    print(f"✅ 所有圖層已儲存至：{save_dir}/")
    return layers


# 測試用
if __name__ == "__main__":
    download_osm_layers("Xitun District, Taichung, Taiwan")
