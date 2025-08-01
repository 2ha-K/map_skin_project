import json
import math
import random
from operator import itemgetter, attrgetter

from PIL import Image

"""
TODO:
1. 自動初始化合理數量的樹木
2. 多行是加速，可以同時檢查多角度
3. 樹木的分配左右上下平衡
"""

def plant_tree(base, tree, x, y, output_path, tree_width, tree_height):
    x_tree_middle = int(x - tree_width // 2)
    y_tree_button = int(y - tree_height)
    base.paste(tree, (x_tree_middle, y_tree_button), mask=tree)#座標位於樹底
    base.save(output_path)
    print(f"✅ 已將樹貼在位置 ({x_tree_middle}, {y_tree_button})：{output_path}")

# 隨機挑選函式version 1.1
def random_picked(green_coordinates,trees_num, tree_height, grid_size):
    """
    在綠地座標中隨機挑選 trees_num 個點，保證平均分布又不擁擠。

    Args:
        green_coordinates (List[Tuple[int, int]]): 綠色區域的像素座標
        trees_num (int): 要挑選的樹數量
        grid_size (int): 格子邊長（單位：像素），數值越大 → 每棵樹越分散

    Returns:
        List[Tuple[int, int]]: 最終挑選的樹木種植座標
    """

    # 1. 將綠地點分類進格子中
    grid = {}
    for x, y in green_coordinates:
        gx = x // grid_size
        gy = y // grid_size
        key = (gx, gy)
        if key not in grid:
            grid[key] = []
        grid[key].append((x, y))

    # 2. 打亂格子順序，在每格挑 1 點，直到選滿
    grid_keys = list(grid.keys())
    random.shuffle(grid_keys)

    selected = []
    for key in grid_keys:
        if len(selected) >= trees_num:
            break
        coord_list = grid[key]
        if coord_list:
            count = 1
            while True:

                chosen = random.choice(coord_list)
                if check_tree_too_close(tree_height, chosen, green_coordinates, selected):
                    print(f"第{count}次嘗試失敗，此點位離非綠地或其他點位太近")
                    count = count + 1
                    if count > 10:
                        print("此區域的點位已經嘗試超過10次，將更換下一個區域")
                        break
                    continue
                selected.append(chosen)
                break

    return selected

def check_tree_too_close(tree_height, coord, green_coordinates, selected):
    trees_space_between = tree_height*0.08
    tree_space_beside = tree_height*0.06

    #檢查是否離非綠地方處太近(由邊界到本點應該都要是綠色)
    cx, cy = coord
    for angle_deg in range(0, 360, 15):
        print(f"{coord}點位檢查: 檢查點位於{angle_deg}度，半徑: {tree_space_beside}處位置是否為綠地")
        angle_rad = math.radians(angle_deg)
        x = int(round(cx + tree_space_beside * math.cos(angle_rad)))
        y = int(round(cy + tree_space_beside * math.sin(angle_rad)))
        if (x, y) not in green_coordinates:
            return True

    for selected_coord in selected:
        print(f"({coord})點位檢查: 檢查與儲備點{selected_coord}的距離是否會太近")
        dist = math.dist(coord, selected_coord)
        if dist < trees_space_between:
            return True
    return False


def random_plant_tree(base, tree, output_path, tree_width, tree_height, green_coordinates, trees_num, grid_size):
    # 先選出10個，這樣排列的方式從上到下才不會樹木覆蓋到葉子
    picked_coordinates = random_picked(green_coordinates, trees_num, tree_height, grid_size)
    sorted_coords = sorted(picked_coordinates, key=itemgetter(1))
    for coord in sorted_coords:
        x, y = coord
        x_tree_middle = int(x - tree_width // 2)
        y_tree_button = int(y - tree_height)
        base.paste(tree, (x_tree_middle, y_tree_button), mask=tree)  # 座標位於樹底

        print(f"樹貼在位置 ({x_tree_middle}, {y_tree_button})")
    base.save(output_path)
    print(f"✅ 已將{trees_num}棵樹樹輸出於：{output_path}")

def plant_trees_at_random_green(
    base_path="output/test_map.png",
    tree_path="assets/park_tree.png",
    output_path="output/test_tree.png",
    map_info_path="output/map_info.json",
    tree_real_world_size_m=100,  # 預設樹在現實中約佔的公尺
    trees_num=10,
    x_start_width_percent = 0,
    x_end_width_percent = 100,
    y_start_width_percent = 0,
    y_end_width_percent = 100,
    grid_size=100
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
    green_coordinates, img_size = get_green_coordinates(base_path)
    my_coordinates = green_coordinates
    if not (x_start_width_percent == 0 and x_end_width_percent == 100 and y_start_width_percent == 0 and y_end_width_percent == 100):
        width, height = img_size
        #由上至下，由左至右
        x_start_pixel = width*x_start_width_percent/100
        x_end_pixel = width*x_end_width_percent/100
        y_start_pixel = height*y_start_width_percent/100
        y_end_pixel = height*y_end_width_percent/100
        my_coordinates = [
            (px, py)
            for px, py in green_coordinates
            if x_start_pixel <= px <= x_end_pixel and y_start_pixel <= py <= y_end_pixel
        ]
    random_plant_tree(base, tree, output_path, tree_size_px * aspect_ratio,tree_size_px, my_coordinates, trees_num, grid_size)

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

    return green_coords, img.size

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