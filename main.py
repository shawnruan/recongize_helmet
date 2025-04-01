import os
import json
import requests
import base64
from PIL import Image
import re
import datetime
from config import API_URL, MODELS, PROMPT_CONFIGS, DATASETS, CATEGORIES, RESULT_DIR

# 确保结果目录存在
os.makedirs(RESULT_DIR, exist_ok=True)

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

def calculate_metrics(predictions, ground_truths):
    """计算二分类指标"""
    tp = fp = fn = tn = 0
    
    for pred, truth in zip(predictions, ground_truths):
        pred_value = pred.get('helmet', 0)
        true_value = truth.get('class', 0)
        
        if pred_value == 1 and true_value == 1:
            tp += 1
        elif pred_value == 1 and true_value == 0:
            fp += 1
        elif pred_value == 0 and true_value == 1:
            fn += 1
        else:  # pred_value == 0 and true_value == 0
            tn += 1
    
    # 计算指标
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn
    }

def process_dataset(base_dir, category, output_prefix, prompt_file, model):
    """处理单个数据集的单个类别"""
    print(f"\n处理数据集: {base_dir}, 类别: {category}")
    print(f"使用模型: {model}")
    print(f"使用提示词配置: {prompt_file}")
    
    image_paths = load_images_and_annotations(base_dir, category)
    predictions = []
    ground_truths = []
    results = []
    
    for image_path, annotation in image_paths:
        print(f"\n处理: {os.path.basename(image_path)}")
        
        prediction = call_api(image_path, prompt_file, model)
        if prediction:
            predictions.append(prediction)
            ground_truths.append(annotation)
            
            results.append({
                "filename": os.path.basename(image_path),
                "prediction": prediction['helmet'],
                "ground_truth": annotation['class']
            })
            
            print(f"预测结果: {prediction}")
            print(f"真实标注: {annotation}")
        else:
            print(f"跳过 {image_path} - 预测失败")
    
    # 计算指标
    metrics = calculate_metrics(predictions, ground_truths)
    
    # 生成报告
    report = {
        "dataset": base_dir,
        "category": category,
        "model": model,
        "prompt_file": prompt_file,
        "total_samples": len(predictions),
        "metrics": metrics,
        "results": results
    }
    
    # 保存报告到结果目录
    output_file = os.path.join(RESULT_DIR, f"{output_prefix}_{category}_report.json")
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=4)
    
    # 打印摘要
    print(f"\n=== {base_dir} - {category} 验证报告 ===")
    print(f"模型: {model}")
    print(f"提示词配置: {prompt_file}")
    print(f"总样本数: {len(predictions)}")
    print(f"Accuracy:  {metrics['accuracy']*100:.2f}%")
    print(f"Precision: {metrics['precision']*100:.2f}%")
    print(f"Recall:    {metrics['recall']*100:.2f}%")
    print(f"F1 Score:  {metrics['f1_score']*100:.2f}%")
    
    return report

def main():
    all_reports = []
    
    # 处理每个模型
    for model in MODELS:
        print(f"\n开始测试模型: {model}")
        
        # 处理每个提示词配置
        for prompt_config in PROMPT_CONFIGS:
            prompt_name = os.path.splitext(os.path.basename(prompt_config))[0]
            print(f"\n使用提示词配置: {prompt_name}")
            
            # 处理每个数据集
            for dataset in DATASETS:
                for category in CATEGORIES:
                    report = process_dataset(
                        dataset, 
                        category,
                        f"validation_{model}_{prompt_name}_{dataset.split('/')[-1].split('_')[0]}",  # 使用模型名、提示词配置和数据集前缀作为输出文件名
                        prompt_config,
                        model
                    )
                    report["prompt_config"] = prompt_name
                    all_reports.append(report)
    
    # 生成汇总报告
    summary_report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total_tests": len(all_reports),
        "models_tested": MODELS,
        "prompt_configs": PROMPT_CONFIGS,
        "reports": all_reports
    }
    
    # 保存汇总报告到结果目录
    summary_report_path = os.path.join(RESULT_DIR, "validation_summary_report.json")
    with open(summary_report_path, 'w') as f:
        json.dump(summary_report, f, indent=4)
    
    print("\n所有模型、数据集和提示词配置测试完成!")
    print(f"详细报告已保存到 {summary_report_path}")

if __name__ == "__main__":
    main()