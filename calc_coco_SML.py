import os
import glob
from PIL import Image
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Relative location of image files directory")
ap.add_argument("-e", "--extension", required=True, help="Relative image files extension name, like jpg, jpeg, png, webp")
ap.add_argument("-t", "--txt", required=True, help="Relative location of yolo txt files directory")
args = vars(ap.parse_args())

def calculate_object_sizes(yolo_dir, img_dir, exts):
  small = medium = large = 0
  total = 0

  # 定義支持的圖片格式
  image_ext = ['jpg', 'jpeg', 'png', 'webp']
  """
  # 獲取基本文件名（不帶擴展名）
  base_name = os.path.splitext(os.path.basename(txt_file))[0]

  # 創建包含所有可能圖片路徑的列表
  image_paths = [os.path.join(img_dir, f"{base_name}.{ext}") for ext in image_ext]
  """
  # 獲取所有標註文件
  for txt_file in glob.glob(os.path.join(yolo_dir, '*.txt')):
    img_file = os.path.join(img_dir, os.path.splitext(os.path.basename(txt_file))[0] + '.' +  exts)
    # img_file = os.path.join(img_dir, os.path.splitext(os.path.basename(txt_file))[0] + '.png')

    if not os.path.exists(img_file):
      continue

    # 獲取圖像尺寸
    with Image.open(img_file) as img:
      img_width, img_height = img.size

    # 讀取YOLO格式的標註
    with open(txt_file, 'r') as f:
      for line in f:
        parts = line.strip().split()
        if len(parts) == 5:  # YOLO format: class x_center y_center width height
          _, _, _, w, h = map(float, parts)

          # 將相對尺寸轉換為絕對像素
          width_pixels = w * img_width
          height_pixels = h * img_height
          area = width_pixels * height_pixels

          # 根據COCO標準分類
          if area < 32*32:
            small += 1
          elif area < 96*96:
            medium += 1
          else:
            large += 1
          total += 1

  # 計算百分比
  if total > 0:
    small_percent = small / total * 100
    medium_percent = medium / total * 100
    large_percent = large / total * 100

    print(f"Small objects: {small_percent:.2f}%")
    print(f"Medium objects: {medium_percent:.2f}%")
    print(f"Large objects: {large_percent:.2f}%")
  else:
    print("No objects found in the dataset.")

# 使用示例
yolo_dir = args["image"]
img_dir = args["txt"]
exts = args["extension"]
calculate_object_sizes(yolo_dir, img_dir, exts)
