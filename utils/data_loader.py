import os
import json

def load_images_and_annotations(base_dir, category):
    """加载图片和对应的标注"""
    images_dir = os.path.join(base_dir, f"{category}_crops")
    json_path = os.path.join(base_dir, f"{category}_annotations.json")
    
    # 读取JSON标注文件
    with open(json_path, 'r') as f:
        annotations = json.load(f) 
    
    # 创建文件名到标注的映射
    annotation_map = {item['filename']: item for item in annotations}
    
    # 收集图片路径
    image_paths = []
    for filename in os.listdir(images_dir):
        if filename.endswith(('.jpg', '.png')):
            image_paths.append((
                os.path.join(images_dir, filename),
                annotation_map.get(filename)
            ))
    
    return image_paths

def load_full_image_and_annotation(directory):
    """加载完整图片及其对应的标注文件"""
    data_pairs = []
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.png')):
            image_path = os.path.join(directory, filename)
            txt_path = os.path.join(directory, filename.replace(filename[-4:], '.txt'))
            
            if os.path.exists(txt_path):
                data_pairs.append((image_path, txt_path))
    return data_pairs

def read_annotations(txt_path):
    """读取标注文件，统计每种类别的数量"""
    counts = {
        "head": 0,
        "helmet": 0,
        "person": 0,
        "alert": False
    }
    
    with open(txt_path, 'r') as f:
        for line in f:
            class_id = int(line.strip().split()[0])
            if class_id == 0:
                counts["head"] += 1
            elif class_id == 1:
                counts["helmet"] += 1
            elif class_id == 2:
                counts["person"] += 1
    
    # 设置alert状态
    counts["alert"] = counts["head"] > 0
    return counts 