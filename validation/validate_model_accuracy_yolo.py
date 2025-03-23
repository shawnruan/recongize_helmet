import os
import json
import requests
import base64
from PIL import Image

def load_image_and_annotation(directory):
    """加载图片及其对应的标注文件"""
    data_pairs = []
    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.png')):
            image_path = os.path.join(directory, filename)
            txt_path = os.path.join(directory, filename.replace(filename[-4:], '.txt'))
            
            if os.path.exists(txt_path):
                data_pairs.append((image_path, txt_path))
    return data_pairs

def read_annotations(txt_path):
    """读取标注文件，统计每种类别的数量并检查是否需要报警"""
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

def call_api(image_path):
    """调用大模型API进行预测"""
    api_url = "http://localhost:11434/api/generate"
    model = "minicpm-v"
    
    with open(image_path, 'rb') as img_file:
        base64_image = base64.b64encode(img_file.read()).decode('utf-8')
        data = {
            "model": model,
            "stream": False,
            "prompt": """分析图片中的人物情况，请严格按照以下规则计数：
            - head: 未戴安全帽的人数
            - helmet: 戴安全帽的人数
            - person: 图片中的总人数（应等于 head + helmet）
            - alert: 是否存在未戴安全帽的情况
            只返回符合以下格式的 JSON：
            {
                "head": <未戴安全帽的人数>,
                "helmet": <戴安全帽的人数>,
                "person": <总人数>,
                "alert": <是否存在未戴安全帽的情况>
            }
            注意：确保 head + helmet = person""",
            "images": [base64_image],
            "format": {
                "type": "object",
                "properties": {
                    "helmet": {
                        "type": "integer"
                    },
                    "head":{
                        "type": "integer"
                    },
                    "person":{
                        "type": "integer"
                    },
                    "alert":{
                        "type": "boolean"
                    }
                },
                "required": [
                    "helmet",
                    "head",
                    "person",
                    "alert"
                ]
            }
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(api_url, json=data, headers=headers)
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
    """计算每个类别的accuracy, precision, recall"""
    metrics = {}
    total_samples = len(predictions)
    
    for class_name in ["head", "helmet", "person", "alert"]:
        if class_name == "alert":
            # alert的二分类指标计算保持不变
            tp = fp = fn = tn = 0
            for pred, truth in zip(predictions, ground_truths):
                pred_value = pred.get(class_name, False)
                true_value = truth[class_name]
                
                if pred_value and true_value:      # True Positive
                    tp += 1
                elif pred_value and not true_value: # False Positive
                    fp += 1
                elif not pred_value and true_value: # False Negative
                    fn += 1
                else:                              # True Negative
                    tn += 1
        else:
            # 对于数值类别(head, helmet, person)，基于总数计算指标
            tp = fp = fn = 0
            tn = 0  # 数值统计中不存在true negative
            
            for pred, truth in zip(predictions, ground_truths):
                pred_count = pred.get(class_name, 0)
                true_count = truth[class_name]
                
                # 计算当前图片中的正确检测、误报和漏检数量
                correct_detections = min(pred_count, true_count)  # 正确检测的数量
                false_positives = max(0, pred_count - true_count) # 误报的数量
                false_negatives = max(0, true_count - pred_count) # 漏检的数量
                
                tp += correct_detections
                fp += false_positives
                fn += false_negatives
        
        # 计算指标
        accuracy = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics[class_name] = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": tn
        }
    
    return metrics

def main():
    directory = "HELMET_SAMPLES_80/obj_train_data"
    data_pairs = load_image_and_annotation(directory)
    
    predictions = []
    ground_truths = []
    
    print("开始处理图片...")
    for image_path, txt_path in data_pairs:
        print(f"\n处理: {os.path.basename(image_path)}")
        
        true_counts = read_annotations(txt_path)
        ground_truths.append(true_counts)
        print(f"真实标注: {true_counts}")
        
        prediction = call_api(image_path)
        if prediction:
            predictions.append(prediction)
            print(f"模型预测: {prediction}")
        else:
            print(f"跳过 {image_path} - 预测失败")
            continue
    
    # 计算详细指标
    metrics = calculate_metrics(predictions, ground_truths)
    
    # 打印详细报告
    print("\n=== 详细验证报告 ===")
    print(f"总样本数: {len(predictions)}")
    
    for class_name, class_metrics in metrics.items():
        print(f"\n{class_name.upper()} 类别指标:")
        print("-" * 40)
        print(f"Accuracy:  {class_metrics['accuracy']*100:.2f}%")
        print(f"Precision: {class_metrics['precision']*100:.2f}%")
        print(f"Recall:    {class_metrics['recall']*100:.2f}%")
        print(f"F1 Score:  {class_metrics['f1_score']*100:.2f}%")
        print("\n详细统计:")
        print(f"True Positives:  {class_metrics['true_positives']}")
        print(f"False Positives: {class_metrics['false_positives']}")
        print(f"False Negatives: {class_metrics['false_negatives']}")
        print(f"True Negatives:  {class_metrics['true_negatives']}")
    
    # 保存详细结果到文件
    results = {
        "total_samples": len(predictions),
        "metrics": metrics,
        "predictions": predictions,
        "ground_truths": ground_truths
    }
    
    with open("validation_results.json", "w") as f:
        json.dump(results, f, indent=4)
    print("\n详细结果已保存到 validation_results.json")

if __name__ == "__main__":
    main()