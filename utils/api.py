import json
import re
import base64
import requests
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

def call_api(image_path, prompt_file, model):
    """调用大模型API进行预测"""
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
                return json.loads(result['response'])
            else:
                print(f"API调用失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"API调用出错: {str(e)}")
            return None 