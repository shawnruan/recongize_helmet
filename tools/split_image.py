import cv2
import os
import json
import shutil

def create_directories(output_base_dir):
    """创建输出目录结构"""
    dirs = {
        'person': os.path.join(output_base_dir, 'person_crops'),
        'head_helmet': os.path.join(output_base_dir, 'head_helmet_crops')
    }
    # 如果输出根目录不存在，创建它
    os.makedirs(output_base_dir, exist_ok=True)
    
    # 创建子目录
    for dir_path in dirs.values():
        os.makedirs(dir_path, exist_ok=True)
    return dirs

def check_head_helmet_in_person(person_box, head_helmet_boxes):
    """检查person框内是否包含helmet"""
    px1, py1, px2, py2 = person_box
    
    for box_type, box in head_helmet_boxes:
        x1, y1, x2, y2 = box
        # 检查框是否大部分在person框内
        if (x1 >= px1 and x2 <= px2 and 
            y1 >= py1 and y2 <= py2):
            if box_type == 1:  # helmet
                return 1
    return 0  # 没有找到helmet或只有head

def crop_and_save_boxes(image_path, txt_path, output_dirs):
    """裁剪框并保存图片和标注"""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image {image_path}")
        return
    
    height, width = image.shape[:2]
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    
    # 读取标注文件
    with open(txt_path, 'r') as f:
        coordinates = [list(map(float, line.strip().split())) for line in f]
    
    # 分类存储boxes
    person_boxes = []
    head_helmet_boxes = []
    
    # 首先收集所有框
    for coord in coordinates:
        class_id = int(coord[0])
        x_center = float(coord[1]) * width
        y_center = float(coord[2]) * height
        box_width = float(coord[3]) * width
        box_height = float(coord[4]) * height
        
        x1 = max(0, int(x_center - box_width/2))
        y1 = max(0, int(y_center - box_height/2))
        x2 = min(width, int(x_center + box_width/2))
        y2 = min(height, int(y_center + box_height/2))
        
        if class_id == 2:  # person
            person_boxes.append((x1, y1, x2, y2))
        elif class_id in [0, 1]:  # head or helmet
            head_helmet_boxes.append((class_id, (x1, y1, x2, y2)))
    
    # 处理和保存crops
    annotations = {
        'person': [],
        'head_helmet': []
    }
    
    # 处理person crops
    for idx, box in enumerate(person_boxes):
        x1, y1, x2, y2 = box
        crop = image[y1:y2, x1:x2]
        if crop.size == 0:
            continue
            
        # 检查person框内是否有helmet
        has_helmet = check_head_helmet_in_person(box, head_helmet_boxes)
        
        # 保存crop
        crop_filename = f"{base_filename}_person_{idx}.jpg"
        crop_path = os.path.join(output_dirs['person'], crop_filename)
        cv2.imwrite(crop_path, crop)
        
        # 添加标注
        annotations['person'].append({
            'filename': crop_filename,
            'class': has_helmet,  # 1 if has helmet, 0 if not
            'bbox': [x1, y1, x2, y2]
        })
    
    # 处理head/helmet crops
    for idx, (class_id, box) in enumerate(head_helmet_boxes):
        x1, y1, x2, y2 = box
        crop = image[y1:y2, x1:x2]
        if crop.size == 0:
            continue
            
        # 保存crop
        crop_filename = f"{base_filename}_{'helmet' if class_id == 1 else 'head'}_{idx}.jpg"
        crop_path = os.path.join(output_dirs['head_helmet'], crop_filename)
        cv2.imwrite(crop_path, crop)
        
        # 添加标注
        annotations['head_helmet'].append({
            'filename': crop_filename,
            'class': class_id,  # 1 for helmet, 0 for head
            'bbox': [x1, y1, x2, y2]
        })
    
    return annotations

def process_directory(input_dir, output_dir):
    """处理输入目录中的图片并将结果保存到输出目录"""
    # 创建输出目录
    output_dirs = create_directories(output_dir)
    
    # 存储所有标注
    all_annotations = {
        'person': [],
        'head_helmet': []
    }
    
    # 处理所有图片
    for filename in os.listdir(input_dir):
        if filename.endswith(('.jpg', '.png')):
            image_path = os.path.join(input_dir, filename)
            txt_path = os.path.join(input_dir, os.path.splitext(filename)[0] + '.txt')
            
            if not os.path.exists(txt_path):
                print(f"Warning: No annotation file found for {filename}")
                continue
            
            print(f"Processing {filename}...")
            
            # 处理图片并获取标注
            annotations = crop_and_save_boxes(image_path, txt_path, output_dirs)
            if annotations:
                all_annotations['person'].extend(annotations['person'])
                all_annotations['head_helmet'].extend(annotations['head_helmet'])
    
    # 保存标注文件到输出目录
    for category in ['person', 'head_helmet']:
        # 保存JSON格式
        json_path = os.path.join(output_dir, f'{category}_annotations.json')
        with open(json_path, 'w') as f:
            json.dump(all_annotations[category], f, indent=4)
        
        # 保存txt格式 (简化格式：filename class)
        txt_path = os.path.join(output_dir, f'{category}_annotations.txt')
        with open(txt_path, 'w') as f:
            for ann in all_annotations[category]:
                f.write(f"{ann['filename']} {ann['class']}\n")
    
    print(f"Processing completed! Results saved to {output_dir}")

if __name__ == "__main__":
    input_directory = "HELMET_SAMPLES_80/obj_train_data"  # 输入目录
    output_directory = "helmet_sample_output_crops"  # 输出目录
    process_directory(input_directory, output_directory)