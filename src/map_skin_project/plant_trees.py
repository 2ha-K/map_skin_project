import json
import random

from PIL import Image

def plant_tree(base, tree, x, y, output_path, tree_width, tree_height):
    x_tree_middle = int(x - tree_width // 2)
    y_tree_button = int(y - tree_height)
    base.paste(tree, (x_tree_middle, y_tree_button), mask=tree)#座標位於樹底
    base.save(output_path)
    print(f"✅ 已將樹貼在位置 ({x_tree_middle}, {y_tree_button})：{output_path}")

def random_plant_tree(base, tree, output_path, tree_width, tree_height, green_coordinates, trees_num):
    # 先選出10個，這樣排列的方式從上到下才不會樹木覆蓋到葉子
    picked_coordinates = random.sample(green_coordinates, trees_num)
    sorted_coords = sorted(picked_coordinates, key=lambda p: p[1], reverse=True)
    for coord in sorted_coords:
        x, y = coord
        x_tree_middle = int(x - tree_width // 2)
        y_tree_button = int(y - tree_height)
        base.paste(tree, (x_tree_middle, y_tree_button), mask=tree)  # 座標位於樹底

        print(f"樹貼在位置 ({x}, {y_tree_button})")
    base.save(output_path)
    print(f"✅ 已將{trees_num}棵樹樹輸出於：{output_path}")

def plant_trees_at_random_green(
    base_path="output/test_map.png",
    tree_path="assets/park_tree.png",
    output_path="output/test_tree.png",
    map_info_path="output/map_info.json",
    tree_real_world_size_m=100,  # 樹在現實中約佔 10 公尺
    trees_num=10
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

    #找出隨機樹個綠色的點種樹
    green_coordinates = get_green_coordinates(base_path)
    random_plant_tree(base, tree, output_path, tree_size_px * aspect_ratio,tree_size_px, green_coordinates, trees_num)


def is_green(pixel):
    r, g, b = pixel
    return g > r and g > b

def get_green_coordinates(image_path):
    """
    回傳圖片中所有綠色像素的座標
    """
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    green_coords = []

    for y in range(height):
        for x in range(width):
            pixel = img.getpixel((x, y))
            if is_green(pixel):
                green_coords.append((x, y))

    return green_coords

def choose_random_coordinate(coords):
    return random.choice(coords) if coords else None

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

    plant_tree(base, tree, x, y, output_path, tree_size_px * aspect_ratio, tree_size_px)

# 測試用
if __name__ == "__main__":
    coordinates = get_green_coordinates("output/test_map.png")
    print(coordinates)