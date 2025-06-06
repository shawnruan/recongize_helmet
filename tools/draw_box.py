import cv2
import numpy as np
import os

def draw_boxes_from_yolo(image_path, txt_path):
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image {image_path}")
        return None
    
    height, width = image.shape[:2]
    
    # 定义不同类别的颜色 (BGR格式)
    colors = {
        0: (255, 0, 0),    # 蓝色 - head
        1: (0, 255, 0),    # 绿色 - helmet
        2: (0, 0, 255),    # 红色 - person
    }
    
    # 读取标注文件
    try:
        with open(txt_path, 'r') as f:
            coordinates = [list(map(float, line.strip().split())) for line in f]
    except Exception as e:
        print(f"Error reading annotation file {txt_path}: {e}")
        return None
    
    # 遍历每个坐标
    for coord in coordinates:
        class_id = int(coord[0])
        x_center = float(coord[1]) * width
        y_center = float(coord[2]) * height
        box_width = float(coord[3]) * width
        box_height = float(coord[4]) * height
        
        # 计算左上角和右下角坐标
        x1 = int(x_center - box_width/2)
        y1 = int(y_center - box_height/2)
        x2 = int(x_center + box_width/2)
        y2 = int(y_center + box_height/2)
        
        # 获取对应类别的颜色
        color = colors.get(class_id, (128, 128, 128))
        
        # 只画框，不添加标签
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    
    return image

def process_directory(input_dir):
    # 遍历目录中的所有文件
    for filename in os.listdir(input_dir):
        # 检查文件是否为jpg或png格式
        if filename.endswith(('.jpg', '.png')):
            # 构建完整的文件路径
            image_path = os.path.join(input_dir, filename)
            # 获取文件扩展名
            file_ext = os.path.splitext(filename)[1]
            txt_path = os.path.join(input_dir, filename.replace(file_ext, '.txt'))
            
            # 检查对应的txt文件是否存在
            if not os.path.exists(txt_path):
                print(f"Warning: No annotation file found for {filename}")
                continue
            
            print(f"Processing {filename}...")
            
            # 处理图片
            result_image = draw_boxes_from_yolo(image_path, txt_path)
            
            if result_image is not None:
                # 构建输出文件路径，保持原始文件扩展名
                output_filename = f"box_{filename}"
                output_path = os.path.join(input_dir, output_filename)
                
                # 保存结果
                cv2.imwrite(output_path, result_image)
                print(f"Saved result to {output_filename}")



# 处理目录
process_directory("HELMET_SAMPLES_80/obj_train_data")
process_directory("LNG_DATASET_SAMPLES_80/obj_train_data")