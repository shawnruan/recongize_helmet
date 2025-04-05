import os
import json
from utils.data_loader import load_images_and_annotations, load_full_image_and_annotation, read_annotations
from utils.api import call_api
from utils.metrics import calculate_metrics
from utils.helpers import get_output_file_path

def process_dataset(base_dir, category, output_prefix, prompt_file, model, experiment_type="crop"):
    """处理单个数据集的单个类别"""
    print(f"\n处理数据集: {base_dir}, 类别: {category if category else '全图'}")
    print(f"使用模型: {model}")
    print(f"使用提示词配置: {prompt_file}")
    print(f"实验类型: {experiment_type}")
    
    if experiment_type == "crop":
        image_paths = load_images_and_annotations(base_dir, category)
    else:
        image_paths = load_full_image_and_annotation(base_dir)
    
    predictions = []
    ground_truths = []
    results = []
    
    for image_path, annotation in image_paths:
        print(f"\n处理: {os.path.basename(image_path)}")
        
        if experiment_type == "crop":
            prediction = call_api(image_path, prompt_file, model)
            if prediction:
                predictions.append(prediction)
                ground_truths.append(annotation)
                
                results.append({
                    "filename": os.path.basename(image_path),
                    "prediction": prediction['helmet'],
                    "ground_truth": annotation['class']
                })
        else:
            # 对于完整图片实验，需要先读取标注
            true_counts = read_annotations(annotation)  # annotation 实际上是 txt_path
            ground_truths.append(true_counts)
            
            prediction = call_api(image_path, prompt_file, model)
            if prediction:
                predictions.append(prediction)
                
                results.append({
                    "filename": os.path.basename(image_path),
                    "prediction": prediction,
                    "ground_truth": true_counts
                })
        
        if prediction:
            print(f"预测结果: {prediction}")
            print(f"真实标注: {annotation if experiment_type == 'crop' else true_counts}")
        else:
            print(f"跳过 {image_path} - 预测失败")
    
    # 计算指标
    metrics = calculate_metrics(predictions, ground_truths, experiment_type)
    
    # 生成报告
    report = {
        "dataset": base_dir,
        "category": category if experiment_type == "crop" else None,
        "model": model,
        "prompt_file": prompt_file,
        "experiment_type": experiment_type,
        "total_samples": len(predictions),
        "metrics": metrics,
        "results": results
    }
    
    # 保存报告到结果目录
    # 对于count类型的实验，使用数据集名称作为标识符
    if experiment_type == "count":
        # 提取数据集名称作为标识符
        dataset_identifier = os.path.basename(base_dir)
        output_file = get_output_file_path(output_prefix, model, dataset_identifier, experiment_type)
    else:
        output_file = get_output_file_path(output_prefix, model, category, experiment_type)
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=4)
    
    # 打印摘要
    print(f"\n=== {base_dir} - {category if experiment_type == 'crop' else '全图分析'} 验证报告 ===")
    print(f"模型: {model}")
    print(f"提示词配置: {prompt_file}")
    print(f"实验类型: {experiment_type}")
    print(f"总样本数: {len(predictions)}")
    
    if experiment_type == "crop":
        print(f"Accuracy:  {metrics['accuracy']*100:.2f}%")
        print(f"Precision: {metrics['precision']*100:.2f}%")
        print(f"Recall:    {metrics['recall']*100:.2f}%")
        print(f"F1 Score:  {metrics['f1_score']*100:.2f}%")
    else:
        for class_name, class_metrics in metrics.items():
            print(f"\n{class_name.upper()} 类别指标:")
            print(f"Accuracy:  {class_metrics['accuracy']*100:.2f}%")
            print(f"Precision: {class_metrics['precision']*100:.2f}%")
            print(f"Recall:    {class_metrics['recall']*100:.2f}%")
            print(f"F1 Score:  {class_metrics['f1_score']*100:.2f}%")
    
    return report 