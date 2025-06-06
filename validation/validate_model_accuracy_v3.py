import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
import json
import base64
from PIL import Image
import time
from datetime import datetime, timedelta
import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from transformers import MultiModalityCasualLM
from deepseek_vl2.models import DeepseekVLV2Processor, DeepseekVLV2ForCausalLM
# 设置代理
# os.environ["HTTP_PROXY"] = "http://your-proxy-address:port"
# os.environ["HTTPS_PROXY"] = "http://your-proxy-address:port"



def format_time(seconds):
    """将秒数转换为可读的时间格式"""
    return str(timedelta(seconds=round(seconds)))

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

# 全局变量存储模型和处理器
MODEL = None
PROCESSOR = None
TOKENIZER = None

def initialize_model(model_path="deepseek-ai/deepseek-vl2-base"):
    """初始化DeepseekVL2模型和处理器"""
    global MODEL, PROCESSOR, TOKENIZER
    
    # 加载处理器
    PROCESSOR = DeepseekVLV2Processor.from_pretrained(model_path)
    TOKENIZER = PROCESSOR.tokenizer
    
    # 加载模型
    MODEL = DeepseekVLV2ForCausalLM.from_pretrained(
        model_path, 
        trust_remote_code=True
    )
    
    # 使用半精度和GPU加速
    if torch.cuda.is_available():
        MODEL = MODEL.to(torch.bfloat16).cuda().eval()
    else:
        MODEL = MODEL.to(torch.bfloat16).eval()
    
    return MODEL, PROCESSOR, TOKENIZER

def call_api(image_path):
    """使用DeepseekVL2模型进行图像分析"""
    global MODEL, PROCESSOR, TOKENIZER
    
    # 首次调用时初始化模型
    if MODEL is None or PROCESSOR is None or TOKENIZER is None:
        MODEL, PROCESSOR, TOKENIZER = initialize_model()
    
    try:
        # 创建对话
        conversation = [
            {
                "role": "<|User|>",
                "content": "请判断图片中的人是否佩戴安全帽。只返回符合以下格式的JSON：{\"helmet\": <是否佩戴安全帽，1表示佩戴，0表示未佩戴>}",
                "images": [image_path],
            },
            {"role": "<|Assistant|>", "content": ""}
        ]
        
        # 加载图像
        image = Image.open(image_path).convert('RGB')
        
        # 准备输入
        prepare_inputs = PROCESSOR(
            conversations=conversation,
            images=[image],
            force_batchify=True,
            system_prompt=""
        ).to(MODEL.device)
        
        # 获取输入嵌入
        inputs_embeds = MODEL.prepare_inputs_embeds(**prepare_inputs)
        
        # 生成回答
        with torch.no_grad():
            outputs = MODEL.language.generate(
                inputs_embeds=inputs_embeds,
                attention_mask=prepare_inputs.attention_mask,
                pad_token_id=TOKENIZER.eos_token_id,
                bos_token_id=TOKENIZER.bos_token_id,
                eos_token_id=TOKENIZER.eos_token_id,
                max_new_tokens=100,
                do_sample=False,
                use_cache=True
            )
        
        # 解码输出
        answer = TOKENIZER.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
        
        # 从回答中提取JSON
        import re
        json_match = re.search(r'\{.*\}', answer, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(0)
            try:
                result = json.loads(json_str)
                return result
            except json.JSONDecodeError:
                print(f"无法解析JSON: {json_str}")
        
        # 如果没有找到JSON格式的回答，尝试从文本中提取结果
        if "佩戴" in answer and "未佩戴" not in answer and "没有佩戴" not in answer:
            return {"helmet": 1}
        elif "未佩戴" in answer or "没有佩戴" in answer:
            return {"helmet": 0}
        else:
            print(f"无法从回答中提取结果: {answer}")
            return None
            
    except Exception as e:
        print(f"处理图像时出错: {str(e)}")
        return None

def calculate_metrics(predictions, ground_truths):
    """计算二分类指标"""
    tp = fp = fn = tn = 0
    
    for pred, truth in zip(predictions, ground_truths):
        pred_value = pred.get('helmet', 0)
        true_value = truth.get('class', 0)
        
        if pred_value == 0 and true_value == 0:
            tp += 1
        elif pred_value == 0 and true_value == 1:
            fp += 1
        elif pred_value == 1 and true_value == 0:
            fn += 1
        else:  # pred_value == 1 and true_value == 1
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

def process_dataset(base_dir, category, output_prefix):
    """处理单个数据集的单个类别"""
    start_time = time.time()
    print(f"\n开始处理数据集: {base_dir}, 类别: {category}")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    image_paths = load_images_and_annotations(base_dir, category)
    predictions = []
    ground_truths = []
    results = []
    
    total_images = len(image_paths)
    processed_images = 0
    
    for image_path, annotation in image_paths:
        img_start_time = time.time()
        processed_images += 1
        
        print(f"\n处理: {os.path.basename(image_path)} ({processed_images}/{total_images})")
        
        prediction = call_api(image_path)
        if prediction:
            predictions.append(prediction)
            ground_truths.append(annotation)
            
            img_time = time.time() - img_start_time
            
            results.append({
                "filename": os.path.basename(image_path),
                "prediction": prediction['helmet'],
                "ground_truth": annotation['class'],
                "processing_time": round(img_time, 2)
            })
            
            print(f"预测结果: {prediction}")
            print(f"真实标注: {annotation}")
            print(f"处理时间: {format_time(img_time)}")
            
            # 估算剩余时间
            avg_time_per_image = (time.time() - start_time) / processed_images
            remaining_images = total_images - processed_images
            estimated_remaining_time = avg_time_per_image * remaining_images
            print(f"预计剩余时间: {format_time(estimated_remaining_time)}")
        else:
            print(f"跳过 {image_path} - 预测失败")
    
    # 计算指标
    metrics = calculate_metrics(predictions, ground_truths)
    
    # 计算总时间
    total_time = time.time() - start_time
    
    # 生成报告
    report = {
        "dataset": base_dir,
        "category": category,
        "total_samples": len(predictions),
        "metrics": metrics,
        "timing": {
            "total_time": round(total_time, 2),
            "average_time_per_image": round(total_time / len(predictions), 2) if predictions else 0,
            "start_time": datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        "results": results
    }
    
    # 保存报告
    output_file = f"{output_prefix}_{category}_report.json"
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=4)
    
    # 打印摘要
    print(f"\n=== {base_dir} - {category} 验证报告 ===")
    print(f"总样本数: {len(predictions)}")
    print(f"总处理时间: {format_time(total_time)}")
    print(f"平均每张处理时间: {format_time(total_time/len(predictions)) if predictions else 'N/A'}")
    print(f"Accuracy:  {metrics['accuracy']*100:.2f}%")
    print(f"Precision: {metrics['precision']*100:.2f}%")
    print(f"Recall:    {metrics['recall']*100:.2f}%")
    print(f"F1 Score:  {metrics['f1_score']*100:.2f}%")
    
    return report

def main():
    total_start_time = time.time()
    
    # 定义数据集路径
    datasets = [
        "helmet_sample_output_crops",
        "lng_output_crops"
    ]
    
    categories = ["person", "head_helmet"]
    
    all_reports = []
    
    # 处理每个数据集的每个类别
    for dataset in datasets:
        for category in categories:
            report = process_dataset(
                dataset, 
                category,
                f"validation_{dataset.split('_')[0]}"
            )
            all_reports.append(report)
    
    total_time = time.time() - total_start_time
    
    print("\n=== 总体统计 ===")
    print(f"总运行时间: {format_time(total_time)}")
    print(f"开始时间: {datetime.fromtimestamp(total_start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    
    print("所有数据集处理完成!")
    print(f"详细报告已保存至 validation_summary_report.json")

if __name__ == "__main__":
    main()