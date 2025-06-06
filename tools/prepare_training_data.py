import json
import os

def prepare_training_data(dataset_info_path, output_path):
    """将数据转换为训练格式"""
    with open(dataset_info_path, 'r') as f:
        dataset = json.load(f)
    
    training_data = []
    for item in dataset:
        # 提取文件名
        image_path = item['image']
        choice = item['choice']
        
        # 构建训练样本
        training_sample = {
            "conversations": [
                {
                    "role": "user",
                    "content": "请判断这张图片中是否有人戴头盔。如果戴了头盔，返回 'helmet'，否则返回 'head'。",
                    "images": [image_path]
                },
                {
                    "role": "assistant",
                    "content": choice
                }
            ]
        }
        training_data.append(training_sample)
    
    # 保存为jsonl格式
    with open(output_path, 'w') as f:
        for item in training_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    dataset_info_path = "validate_dataset.json"
    output_path = "training_data.jsonl"
    prepare_training_data(dataset_info_path, output_path)
