import json
import re
import base64
import requests
import time
from config import API_URL

def load_prompt_config(markdown_file):
    """从 markdown 文件中加载 prompt 和 format 配置"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 prompt
    prompt_match = re.search(r'```prompt\n(.*?)\n```', content, re.DOTALL)
    prompt = prompt_match.group(1).strip() if prompt_match else None
    
    # 提取 format
    format_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
    format_config = json.loads(format_match.group(1)) if format_match else None
    

    
    return prompt, format_config

def validate_prediction(prediction, experiment_type="crop"):
    """验证预测结果的合法性"""
    if prediction is None:
        return None
    
    if experiment_type == "crop":
        # 对于裁剪图片实验，helmet值应该是0或1
        if 'helmet' in prediction and prediction['helmet'] not in [0, 1]:
            print(f"警告: 异常的helmet值: {prediction['helmet']}，将被修正为二进制值")
            prediction['helmet'] = 1 if prediction['helmet'] > 0.5 else 0
    elif experiment_type == "binary":
        # 对于二分类实验，helmet_score值应该在1到100之间
        if 'helmet_score' in prediction:
            try:
                score_value = int(prediction['helmet_score'])
                # 确保分数在1到100之间
                if score_value < 1 or score_value > 100:
                    print(f"警告: 异常的helmet_score值: {score_value}，将被限制在1到100之间")
                    prediction['helmet_score'] = max(1, min(score_value, 100))
                else:
                    prediction['helmet_score'] = score_value
                
                # 将分数转换为概率值 (1-100 -> 0.01-1.0)
                prediction['helmet_probability'] = prediction['helmet_score'] / 100.0
                
            except (ValueError, TypeError):
                print(f"警告: 无法将helmet_score值转换为整数: {prediction['helmet_score']}，将被设置为1")
                prediction['helmet_score'] = 1
                prediction['helmet_probability'] = 0.01  # 设置最小概率
    else:
        # 对于数量统计实验，检查各计数值是否合理
        for field in ['head', 'helmet', 'person']:
            if field in prediction:
                try:
                    # 尝试转换为整数
                    value = int(float(prediction[field])) if prediction[field] is not None else 0
                    # 检查是否在合理范围内（假设一张图片不会有超过10个人/头/帽子）
                    if value < 0 or value > 10:
                        print(f"警告: 异常的{field}值: {prediction[field]}，将被限制在合理范围内")
                        prediction[field] = max(0, min(value, 10))
                    else:
                        prediction[field] = value
                except (ValueError, TypeError):
                    print(f"警告: 无法将{field}值转换为数字: {prediction[field]}，将被设置为0")
                    prediction[field] = 0
        
        # 确保alert是布尔值
        if 'alert' in prediction and not isinstance(prediction['alert'], bool):
            print(f"警告: alert不是布尔值: {prediction['alert']}，将被转换为布尔值")
            prediction['alert'] = bool(prediction['alert'])
    
    return prediction

def call_api(image_path, prompt_file, model, experiment_type="crop"):
    """调用大模型API进行预测"""
    # 记录开始时间
    start_time = time.time()
    
    # 加载 prompt 和 format 配置
    prompt, format_config = load_prompt_config(prompt_file)
    if not prompt or not format_config:
        raise ValueError("无法从配置文件加载 prompt 或 format 配置")
    
    with open(image_path, 'rb') as img_file:
        base64_image = base64.b64encode(img_file.read()).decode('utf-8')
        data = {
            "model": model,
            "stream": False,
            "prompt": prompt,
            "images": [base64_image],
            "format": format_config
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(API_URL, json=data, headers=headers)
            if response.status_code == 200:
                result = response.json()
                prediction = json.loads(result['response'])
                # 验证并修正预测结果
                validated_prediction = validate_prediction(prediction, experiment_type)
                
                # 记录结束时间并计算耗时
                end_time = time.time()
                inference_time = end_time - start_time
                
                # 将推理时间添加到预测结果中
                if validated_prediction:
                    validated_prediction['inference_time'] = round(inference_time, 3)
                
                return validated_prediction
            else:
                print(f"API调用失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"API调用出错: {str(e)}")
            return None 