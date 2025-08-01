import json
from PIL import Image

def plant_tree(base, tree, x, y, output_path, tree_height):
    y_tree_button = y-tree_height//2
    base.paste(tree, (x, y_tree_button), mask=tree)#座標位於樹底
    base.save(output_path)
    print(f"✅ 已將樹貼在位置 ({x}, {y_tree_button})：{output_path}")

def plant_a_tree_in_center(
    base_path="output/test_map.png",
    tree_path="assets/park_tree.png",
    output_path="output/test_tree.png",
    map_info_path="output/map_info.json",
    tree_real_world_size_m=100  # 樹在現實中約佔 10 公尺
):
    # 讀取底圖與樹圖
    base = Image.open(base_path).convert("RGBA")
    tree = Image.open(tree_path).convert("RGBA")

    # 讀取地圖比例資訊
    with open(map_info_path, "r") as f:
        info = json.load(f)
        degrees_per_pixel = info["degrees_per_pixel"]

    # 假設 1 度 ≈ 111,000 公尺（緯度換算）
    meters_per_pixel = degrees_per_pixel * 111_000
    tree_size_px = int(tree_real_world_size_m / meters_per_pixel)

    # 按照原始長寬比縮放
    aspect_ratio = tree.width / tree.height
    tree = tree.resize((int(tree_size_px * aspect_ratio), tree_size_px), resample=Image.Resampling.LANCZOS)

    # 貼在正中央
    bw, bh = base.size
    tw, th = tree.size
    x = (bw - tw) // 2
    y = (bh - th) // 2

    plant_tree(base, tree, x, y, output_path, tree_size_px)
