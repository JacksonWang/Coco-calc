import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--txt", required=True, help="Relative location of yolo txt files directory")
args = vars(ap.parse_args())


def count_classes(label_dir):
  class_counts = {}

  # 標籤目錄中的所有文件
  for label_file in os.listdir(label_dir):
    if label_file.endswith('.txt'):  # 確保是標籤文件
      with open(os.path.join(label_dir, label_file), 'r') as f:
        for line in f:
          class_id = int(line.split()[0])  # 假設類別 ID 是行的第一個數字
          if class_id in class_counts:
            class_counts[class_id] += 1
          else:
            class_counts[class_id] = 1

  return class_counts

label_directory = args["txt"]
counts = count_classes(label_directory)

# 輸出結果
for class_id, count in counts.items():
    print(f'Class {class_id}: {count} items')
