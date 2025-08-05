import os
import osmnx as ox
from shapely.geometry import box
from shapely.lib import distance

from map_skin_project.map_utils import ensure_path, save_map_metadata, km_to_latitude_degrees, km_to_longitude_degrees, delete_file_by_name

def download_osm_layers(
    place_name: str = None,
    mode: str = "location",
    bbox: tuple = None,  # (minx, miny, maxx, maxy) 在 Python 中，tuple（元組）是一種**不可變（immutable）**的序列資料型別，功能類似 list，但不能修改其中的元素。
    center_longitude_latitude: tuple = None,
    width_km: float =0.5,
    height_km: float = 0.5,
    save_dir: str = "data",

):
    """
    根據地名或經緯度邊界下載 OSM 圖層。


    TODO: 加強精準度, 座標定位版本, 更層級的精準配合, 改成向osm map的比例尺形式, 圖片大小(🛠️ 範例程式：使用 gdf.clip(...) 裁切所有圖層)
    https://wiki.openstreetmap.org/wiki/Zh-hant:Map_Features
    根據地名下載 OSM 圖層並各自儲存為 GeoJSON，適用於遊戲地圖製作。

    Args:
        place_name (str): 地名，例如 "Xinyi District, Taipei, Taiwan"
        save_dir (str): 儲存資料夾
        mode: "location" | "bbox"
        - location: 使用 place_name 下載
        - Longitude_Latitude: 鎖定經緯度的一個範圍下載
        - bbox: 使用經緯度範圍下載
        bbox: (minx, miny, maxx, maxy)
        center_longitude_latitude: (Longitude, Latitude)
        width_km: 要多少公里寬
        height_km: 要多少公尺高
    Returns:
        dict: 包含各圖層名稱與對應 GeoDataFrame 的字典
    """
    os.makedirs(save_dir, exist_ok=True)
    layers = {}

    if mode == "location":
        query_area = place_name
        query_func = ox.features.features_from_place
        bbox_geom = None #假設: 命名取地區會自動截掉
    elif mode == "bbox":
        query_area = bbox
        query_func = ox.features.features_from_bbox
        minx, miny, maxx, maxy = bbox
        bbox_geom = box(minx, miny, maxx, maxy) # 用於截掉過長的圖層
    elif mode == "longitude_latitude":
        cx, cy = center_longitude_latitude
        minx = cx-km_to_longitude_degrees(width_km/2, cy)
        miny = cy-km_to_latitude_degrees(height_km/2)
        maxx = cx+km_to_longitude_degrees(width_km/2, cy)
        maxy = cy+km_to_latitude_degrees(height_km/2)
        set_bbox = (minx, miny, maxx, maxy)
        query_area = set_bbox
        query_func = ox.features.features_from_bbox
        bbox_geom = box(minx, miny, maxx, maxy) # 用於截掉過長的圖層
    else:
        raise ValueError(f"Unsupported mode: {mode}")

    # 公園（leisure=park or playground）
    print("🌳 下載公園與綠地...")
    try:
        gdf_parks = query_func(query_area, tags={
            "leisure": True,
            "landuse": True,
            "natural": ["grassland", "wood"]
        })
        if bbox_geom is not None:
            gdf_parks = gdf_parks.clip(bbox_geom)
        gdf_parks.to_file(ensure_path(save_dir, "parks.geojson"), driver="GeoJSON")
        layers["parks"] = gdf_parks

        save_scale(gdf_parks)  # 儲存比例尺
    except Exception as e:
        print(f"⚠️ parks 下載失敗：{e}")
        delete_file_by_name(save_dir, "parks.geojson")
        exit("沒有綠地無法存取比例尺")

    # 建築物
    print("🏢 下載建築物...")
    try:
        gdf_building = query_func(query_area, tags={"building": True})
        if bbox_geom is not None:
            gdf_building = gdf_building.clip(bbox_geom)
        gdf_building.to_file(ensure_path(save_dir, "buildings.geojson"), driver="GeoJSON")
        layers["buildings"] = gdf_building
    except Exception as e:
        print(f"⚠️ building 下載失敗：{e}")
        delete_file_by_name(save_dir, "buildings.geojson")

    # 道路（各級道路）
    print("🛣️ 下載道路...")
    try:
        road_types = [
            "motorway", "trunk", "primary", "secondary", "tertiary",
            "residential", "unclassified", "service", "living_street",
            "pedestrian", "footway", "cycleway", "path"
        ]
        gdf_roads = query_func(query_area, tags={"highway": road_types})
        if bbox_geom is not None:
            gdf_roads = gdf_roads.clip(bbox_geom)
        gdf_roads.to_file(ensure_path(save_dir, "roads.geojson"), driver="GeoJSON")
        layers["roads"] = gdf_roads
    except Exception as e:
        print(f"⚠️ highway 下載失敗：{e}")

    # 河流、湖泊（natural=water or waterway）
    print("🌊 下載水體（水域）...")
    try:
        gdf_water = query_func(query_area, tags={"natural": "water"})
        if bbox_geom is not None:
            gdf_water = gdf_water.clip(bbox_geom)
        gdf_water.to_file(ensure_path(save_dir, "water.geojson"), driver="GeoJSON")
        layers["water"] = gdf_water
    except Exception as e:
        print(f"⚠️ water 下載失敗：{e}")
        delete_file_by_name(save_dir, "water.geojson")

    # 河川與溪流（流動水體）
    print("🛶 下載河流與溪流...")
    try:
        gdf_rivers = query_func(query_area, tags={"waterway": True})
        if bbox_geom is not None:
            gdf_rivers = gdf_rivers.clip(bbox_geom)
        gdf_rivers.to_file(ensure_path(save_dir, "rivers.geojson"), driver="GeoJSON")
        layers["rivers"] = gdf_rivers
    except Exception as e:
        print(f"⚠️ rivers 下載失敗：{e}")
        delete_file_by_name(save_dir, "rivers.geojson")

    # 森林或樹林區（natural=wood）
    print("🌲 下載森林區...")
    try:
        gdf_wood = query_func(query_area, tags={"natural": "wood"})
        if bbox_geom is not None:
            gdf_wood = gdf_wood.clip(bbox_geom)
        gdf_wood.to_file(ensure_path(save_dir, "forest.geojson"), driver="GeoJSON")
        layers["forest"] = gdf_wood
    except Exception as e:
        print(f"⚠️ wood 下載失敗：{e}")
        delete_file_by_name(save_dir, "forest.geojson")

    # 可選：地標（POI）
    # print("📍下載學校與車站...")
    # gdf_poi = query_func(query_area, tags={"amenity": ["school", "bus_station"]})
    # gdf_poi.to_file(ensure_path(save_dir, "poi.geojson"), driver="GeoJSON")
    # layers["poi"] = gdf_poi

    print(f"✅ 所有圖層已儲存至：{save_dir}/")
    return layers

def save_scale(gdf_parks):
    minx, miny, maxx, maxy = gdf_parks.total_bounds
    geo_width = maxx - minx
    geo_height = maxy - miny
    degrees_per_pixel = geo_width / 6000

    metadata = {
        "geo_width_deg": geo_width,
        "geo_height_deg": geo_height,
        "degrees_per_pixel": degrees_per_pixel,
    }

    save_metadata_dir = "output/map_info.json"
    save_map_metadata(filepath=save_metadata_dir, metadata=metadata)
    print(f"✅ 已建立比例尺於：{save_metadata_dir}/")


# 測試用
if __name__ == "__main__":
    download_osm_layers("Xitun District, Taichung, Taiwan")
