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
    return re.sub(r'\W+', '_', name.lower()).strip('_')