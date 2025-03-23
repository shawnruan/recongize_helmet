# Author:@ruanxiaoyang
# 调用ollama在本地的api,读取在本地test_img下的png图片，生成head或者helmet的结果，然后在dataset_info.json中读取对应的结果，验证模型的正确率


import os
import json
import requests
import base64
from PIL import Image

def load_images_from_directory(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            img_path = os.path.join(directory, filename)
            images.append(img_path)
    return images

def call_api(image_path):
    api_url = "http://localhost:11434/api/generate"  # Ollama 推理 API 端点
    model = "minicpm-v"  # 使用适合处理图片的模型，如 LLaVA（Large Language and Vision Assistant）
        
    with open(image_path, 'rb') as img_file:
        # 读取并转换图片为 Base64
        base64_image = base64.b64encode(img_file.read()).decode('utf-8')
        data = {
            "model": model,
            "stream": False,
            "prompt": "请判断这张图片中是否有人戴头盔。如果戴了头盔，返回 'helmet' 的值为true, 否则返回 'helmet' 的值为false,Respond using JSON",
            "images": [base64_image],
            "format": {
                "type": "object",
                "properties": {
                    "helmet": {
                        "type": "boolean"
                    }
                },
                "required": [
                    "helmet"
                ]
            }
        }
        
        headers = {
            "Content-Type": "application/json"
        }
    
        response = requests.post(api_url, data=json.dumps(data), headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            # 添加文件名到返回结果中
            result['filename'] = os.path.basename(image_path)
            print(result)
            return result
        else:
            return {
                'filename': os.path.basename(image_path),
                'prediction': None,
                
                'error': response.text  # 记录错误信息
            }
   

def validate_model_accuracy(results, dataset_info_path):
    with open(dataset_info_path, 'r') as json_file:
        dataset_info = json.load(json_file)
    
    # 创建查找字典，key为文件名，value为预期结果
    lookup_dict = {}
    for info in dataset_info:
        info_filename = os.path.basename(info['image'])
        if '-' in info_filename:
            info_filename = info_filename.split('-', 1)[1]
        lookup_dict[info_filename] = (info['choice'] == 'helmet')
    
    correct_predictions = 0
    total_predictions = len(results)
    error_predictions = []  # 收集错误预测

    for result in results:
        filename = result['filename']
        if filename in lookup_dict:
            api_result = json.loads(result['response'])['helmet']
            expected = lookup_dict[filename]
            if api_result == lookup_dict[filename]:
                correct_predictions += 1
            else:
                error_predictions.append({
                    'filename': filename,
                    'prediction': 'helmet' if api_result else 'head',
                    'ground_truth': 'helmet' if expected else 'head'
                })    
            

    accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
    
    # 打印完整报告
    print("\n=== 模型验证报告 ===")
    print(f"总样本数: {total_predictions}")
    print(f"正确预测: {correct_predictions}")
    print(f"错误预测: {len(error_predictions)}")
    print(f"准确率: {accuracy * 100:.2f}%")
    
    if error_predictions:
        print("\n错误预测详情:")
        print("-" * 50)
        for error in error_predictions:
            print(f"文件名: {error['filename']}")
            print(f"预测结果: {error['prediction']}")
            print(f"实际标注: {error['ground_truth']}")
            print("-" * 50)
    return accuracy

def main():
    directory = './validate_img'
    dataset_info_path = 'validate_dataset.json'
    
    images = load_images_from_directory(directory)
    results = []

    for image in images:
        result = call_api(image)
        results.append(result)

    validate_model_accuracy(results, dataset_info_path)
    


if __name__ == "__main__":  # 添加这一行以执行主函数
    main()