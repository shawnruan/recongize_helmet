import json
import re
import base64
import requests
import os
import torch
from io import BytesIO
from PIL import Image
from config import API_URL, TRANSFORMER_MODEL_PATH

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
    else:
        # 对于数量统计实验，检查各计数值是否合理
        for field in ['head', 'helmet', 'person']:
            if field in prediction:
                try:
                    # 尝试转换为整数
                    value = int(float(prediction[field])) if prediction[field] is not None else 0
                    # 检查是否在合理范围内（假设一张图片不会有超过100个人/头/帽子）
                    if value < 0 or value > 100:
                        print(f"警告: 异常的{field}值: {prediction[field]}，将被限制在合理范围内")
                        prediction[field] = max(0, min(value, 100))
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
                return validated_prediction
            else:
                print(f"API调用失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"API调用出错: {str(e)}")
            return None

def call_transformer_api(image_path, prompt_file, model_name, experiment_type="crop"):
    """使用 Transformer 模型进行预测
    
    Args:
        image_path: 图片路径
        prompt_file: 提示词文件路径
        model_name: 模型名称，可以是本地路径或 HuggingFace 模型ID
        experiment_type: 实验类型，"crop" 或 "count"
        
    Returns:
        预测结果，格式与 call_api 函数相同
    """
    try:
        # 加载 prompt 配置
        prompt, format_config = load_prompt_config(prompt_file)
        if not prompt or not format_config:
            raise ValueError("无法从配置文件加载 prompt 或 format 配置")
        
        # 根据是否存在本地模型路径决定加载方式
        if os.path.exists(model_name):
            # 本地模型
            print(f"使用本地模型: {model_name}")
            from transformers import AutoProcessor, AutoModelForCausalLM
            processor = AutoProcessor.from_pretrained(model_name)
            model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
        else:
            # HuggingFace 模型
            print(f"使用 HuggingFace 模型: {model_name}")
            from transformers import pipeline
            pipe = pipeline("image-to-text", model=model_name, device_map="auto")
            
            # 读取图片
            image = Image.open(image_path)
            
            # 使用管道直接生成文本
            outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 512})
            if isinstance(outputs, list) and len(outputs) > 0:
                text_output = outputs[0].get("generated_text", "")
            else:
                text_output = outputs
                
            # 尝试从文本中提取 JSON
            try:
                # 查找 JSON 对象
                json_match = re.search(r'(\{.*\})', text_output, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    prediction = json.loads(json_str)
                    validated_prediction = validate_prediction(prediction, experiment_type)
                    return validated_prediction
                else:
                    print(f"无法从输出中提取 JSON 对象: {text_output}")
                    return None
            except json.JSONDecodeError:
                print(f"JSON 解析失败: {text_output}")
                return None
            
        # 以下代码适用于本地模型的加载方式
        # 读取并处理图像
        image = Image.open(image_path)
        inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)
        
        # 生成输出
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=False
            )
        
        # 解码输出
        generated_text = processor.batch_decode(outputs, skip_special_tokens=True)[0]
        
        # 尝试从生成的文本中提取 JSON
        try:
            # 查找 JSON 对象
            json_match = re.search(r'(\{.*\})', generated_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
                prediction = json.loads(json_str)
                validated_prediction = validate_prediction(prediction, experiment_type)
                return validated_prediction
            else:
                print(f"无法从输出中提取 JSON 对象: {generated_text}")
                return None
        except json.JSONDecodeError:
            print(f"JSON 解析失败: {generated_text}")
            return None
    
    except Exception as e:
        print(f"Transformer 模型调用出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def call_llm_studio_api(image_path, prompt_file, model_name, api_url, api_key=None, experiment_type="crop"):
    """使用 LLM Studio API 进行预测
    
    Args:
        image_path: 图片路径
        prompt_file: 提示词文件路径
        model_name: 模型名称
        api_url: LLM Studio API URL
        api_key: API 密钥 (可选)
        experiment_type: 实验类型，"crop" 或 "count"
        
    Returns:
        预测结果，格式与 call_api 函数相同
    """
    try:
        # 加载 prompt 配置
        prompt, format_config = load_prompt_config(prompt_file)
        if not prompt or not format_config:
            raise ValueError("无法从配置文件加载 prompt 或 format 配置")
        
        # 读取图片，转换为 base64
        with open(image_path, 'rb') as img_file:
            base64_image = base64.b64encode(img_file.read()).decode('utf-8')
        
        # 构建请求数据
        data = {
            "model": model_name,
            "prompt": prompt,
            "images": [base64_image],
            "max_tokens": 1024,
            "temperature": 0.01,  # 低温度，更确定性的输出
            "format": format_config if format_config else {}
        }
        
        # 构建请求头
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        # 发送请求
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            # LLM Studio 可能有不同的响应格式，需要根据实际情况调整
            if "response" in result:
                # 类似 Ollama 格式
                prediction_text = result["response"]
            elif "choices" in result and len(result["choices"]) > 0:
                # 类似 OpenAI 格式
                prediction_text = result["choices"][0]["message"]["content"]
            else:
                # 其他格式，直接使用结果
                prediction_text = str(result)
            
            # 尝试从文本中提取 JSON
            try:
                # 首先尝试直接解析整个文本
                try:
                    prediction = json.loads(prediction_text)
                except json.JSONDecodeError:
                    # 如果失败，尝试在文本中查找 JSON 对象
                    json_match = re.search(r'(\{.*\})', prediction_text, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1)
                        prediction = json.loads(json_str)
                    else:
                        print(f"无法从输出中提取 JSON 对象: {prediction_text}")
                        return None
                
                # 验证并修正预测结果
                validated_prediction = validate_prediction(prediction, experiment_type)
                return validated_prediction
            except json.JSONDecodeError:
                print(f"JSON 解析失败: {prediction_text}")
                return None
        else:
            print(f"LLM Studio API 调用失败: {response.status_code}")
            print(response.text)
            return None
    
    except Exception as e:
        print(f"LLM Studio 调用出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return None 