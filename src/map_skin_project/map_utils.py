import math
from pathlib import Path
import re

def ensure_path(directory: str, filename: str) -> Path:
    """
    建立目錄並回傳組合後的完整路徑。

    Args:
        directory (str): 資料夾名稱
        filename (str): 檔案名稱（例如 map.geojson）

    Returns:
        Path: 完整的儲存路徑
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path / filename

def slugify(name: str):
    return re.sub(r'[^\w\u4e00-\u9fff]+', '_', name.lower()).strip('_')

import json

def save_map_metadata(filepath: str, metadata: dict):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

import math

def km_to_latitude_degrees(km):
    return km / 111

def km_to_longitude_degrees(km, latitude_deg):
    return km / (111 * math.cos(math.radians(latitude_deg)))

import os

def delete_file_by_name(folder_path, filename):
    """
    刪除指定資料夾下指定檔名的檔案（不含子資料夾）

    Args:
        folder_path (str): 資料夾路徑
        filename (str): 完整檔案名稱，例如 "buildings.geojson"
    """
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
            print(f"✅ 已刪除舊的檔案檔案：{file_path}")
        except Exception as e:
            print(f"⚠️ 無法刪除舊檔案 {file_path}：{e}")
    else:
        print(f"ℹ️ 尚未有舊的檔案：{file_path}")





# 測試用
if __name__ == "__main__":
    print(slugify("清華大學, 新竹市, 台灣"))
