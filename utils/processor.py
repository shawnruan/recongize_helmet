import os
import json
import time
from utils.data_loader import load_images_and_annotations, load_full_image_and_annotation, read_annotations
from utils.api import call_api
from utils.metrics import calculate_metrics
from utils.helpers import get_output_file_path
from utils.visualization import plot_score_distribution
from config import BINARY_THRESHOLD

def process_dataset(base_dir, category, output_prefix, prompt_file, model, experiment_type="crop"):
    """处理单个数据集的单个类别"""
    # 记录开始时间
    start_time = time.time()
    
    print(f"\n处理数据集: {base_dir}, 类别: {category if category else 'full_image'}")
    print(f"使用模型: {model}")
    print(f"使用提示词配置: {prompt_file}")
    print(f"实验类型: {experiment_type}")
    
    if experiment_type in ["crop", "binary"]:
        image_paths = load_images_and_annotations(base_dir, category)
    else:
        image_paths = load_full_image_and_annotation(base_dir)
    
    predictions = []
    ground_truths = []
    results = []
    
    # 记录成功处理的图片数量
    successful_predictions = 0
    total_inference_time = 0
    
    for image_path, annotation in image_paths:
        print(f"\n处理: {os.path.basename(image_path)}")
        
        if experiment_type == "crop":
            prediction = call_api(image_path, prompt_file, model, experiment_type)
            if prediction:
                predictions.append(prediction)
                ground_truths.append(annotation)
                
                # 记录推理时间
                inference_time = prediction.get('inference_time', 0)
                total_inference_time += inference_time
                successful_predictions += 1
                
                results.append({
                    "filename": os.path.basename(image_path),
                    "prediction": prediction['helmet'],
                    "ground_truth": annotation['class'],
                    "inference_time": inference_time
                })
        elif experiment_type == "binary":
            prediction = call_api(image_path, prompt_file, model, experiment_type)
            if prediction:
                predictions.append(prediction)
                ground_truths.append(annotation)
                
                # 记录推理时间
                inference_time = prediction.get('inference_time', 0)
                total_inference_time += inference_time
                successful_predictions += 1
                
                # 获取详细分数并计算总分
                detailed_scores = prediction.get('detailed_scores', {})
                if detailed_scores:
                    # 如果存在详细分数，则将其相加作为总分
                    calculated_score = sum(detailed_scores.values())
                    # 更新 helmet_score 以确保其为详细分数的总和
                    prediction['helmet_score'] = calculated_score
                    # 计算概率值 (将分数转换为0.01-1.0范围)
                    prob_value = calculated_score / 100.0
                    prediction['helmet_probability'] = prob_value
                else:
                    # 如果没有详细分数，则使用原始分数
                    original_score = prediction.get('helmet_score', 0)
                    prob_value = prediction.get('helmet_probability', original_score / 100.0)
                
                binary_result = 1 if prob_value >= BINARY_THRESHOLD else 0
                
                results.append({
                    "filename": os.path.basename(image_path),
                    "score": prediction.get('helmet_score', 0),  # 更新后的总分
                    "probability": prob_value,  # 更新后的概率值
                    "binary_prediction": binary_result,
                    "ground_truth": annotation['class'],
                    "inference_time": inference_time
                })
        else:
            # 对于完整图片实验，需要先读取标注
            true_counts = read_annotations(annotation)  # annotation 实际上是 txt_path
            ground_truths.append(true_counts)
            
            prediction = call_api(image_path, prompt_file, model, experiment_type)
            if prediction:
                predictions.append(prediction)
                
                # 记录推理时间
                inference_time = prediction.get('inference_time', 0)
                total_inference_time += inference_time
                successful_predictions += 1
                
                results.append({
                    "filename": os.path.basename(image_path),
                    "prediction": prediction,
                    "ground_truth": true_counts,
                    "inference_time": inference_time
                })
        
        if prediction:
            print(f"预测结果: {prediction}")
            
            # 对于二分类实验，额外显示概率信息
            if experiment_type == "binary":
                score = prediction.get('helmet_score', 0)
                prob = prediction.get('helmet_probability', 0)
                threshold = BINARY_THRESHOLD
                binary_result = 1 if prob >= threshold else 0
                print(f"分数: {score}/100，概率: {prob:.2f}，阈值: {threshold}，结果: {'戴安全帽' if binary_result == 1 else '未戴安全帽'}")
                
            print(f"真实标注: {annotation if experiment_type in ['crop', 'binary'] else true_counts}")
            print(f"推理时间: {prediction.get('inference_time', 0):.3f}秒")
        else:
            print(f"跳过 {image_path} - 预测失败")
    
    # 计算指标
    metrics = calculate_metrics(predictions, ground_truths, experiment_type)
    
    # 计算总时间和平均时间
    total_time = time.time() - start_time
    avg_inference_time = total_inference_time / successful_predictions if successful_predictions > 0 else 0
    
    # 生成报告
    report = {
        "dataset": base_dir,
        "category": category if experiment_type == "crop" else None,
        "model": model,
        "prompt_file": prompt_file,
        "experiment_type": experiment_type,
        "total_samples": len(predictions),
        "metrics": metrics,
        "timing": {
            "total_time": round(total_time, 3),
            "total_inference_time": round(total_inference_time, 3),
            "average_inference_time": round(avg_inference_time, 3),
            "successful_predictions": successful_predictions
        },
        "results": results
    }
    
    # 保存报告到结果目录
    # 对于count类型的实验，使用数据集名称作为标识符
    if experiment_type == "count":
        # 提取数据集名称作为标识符
        dataset_identifier = os.path.basename(base_dir)
        output_file = get_output_file_path(output_prefix, model, dataset_identifier, experiment_type, prompt_file)
    else:
        output_file = get_output_file_path(output_prefix, model, category, experiment_type, prompt_file)
    
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=4)
    
    # 如果是二分类实验，生成分数分布图
    if experiment_type == "binary" and results:
        prompt_basename = os.path.basename(prompt_file)
        plot_paths = plot_score_distribution(
            results, 
            base_dir, 
            category, 
            model, 
            prompt_basename, 
            experiment_type
        )
        
        if plot_paths:
            # 将分布图路径添加到报告中
            report["distribution_plots"] = plot_paths
    
    # 打印摘要
    print(f"\n=== {base_dir} - {category if experiment_type in ['crop', 'binary'] else 'full_image'} 验证报告 ===")
    print(f"模型: {model}")
    print(f"提示词配置: {prompt_file}")
    print(f"实验类型: {experiment_type}")
    print(f"总样本数: {len(predictions)}")
    print(f"总处理时间: {total_time:.3f}秒")
    print(f"总推理时间: {total_inference_time:.3f}秒")
    print(f"平均推理时间: {avg_inference_time:.3f}秒/张")
    
    if experiment_type in ["crop", "binary"]:
        print(f"Accuracy:  {metrics['accuracy']*100:.2f}%")
        print(f"Precision: {metrics['precision']*100:.2f}%")
        print(f"Recall:    {metrics['recall']*100:.2f}%")
        print(f"F1 Score:  {metrics['f1_score']*100:.2f}%")
        
        # 对于crop实验，显示详细的类别指标和F1_macro
        if experiment_type == "crop":
            print(f"\n=== 详细类别指标 ===")
            print(f"Head类别:")
            print(f"  Precision: {metrics['head_precision']*100:.2f}%")
            print(f"  Recall:    {metrics['head_recall']*100:.2f}%")
            print(f"  F1 Score:  {metrics['head_f1']*100:.2f}%")
            print(f"Helmet类别:")
            print(f"  Precision: {metrics['helmet_precision']*100:.2f}%")
            print(f"  Recall:    {metrics['helmet_recall']*100:.2f}%")
            print(f"  F1 Score:  {metrics['helmet_f1']*100:.2f}%")
            print(f"\nF1 Macro:  {metrics['f1_macro']*100:.2f}%")
        
        if experiment_type == "binary":
            print(f"分类阈值: {metrics['threshold']}")
    else:
        for class_name, class_metrics in metrics.items():
            print(f"\n{class_name.upper()} 类别指标:")
            print(f"Accuracy:  {class_metrics['accuracy']*100:.2f}%")
            print(f"Precision: {class_metrics['precision']*100:.2f}%")
            print(f"Recall:    {class_metrics['recall']*100:.2f}%")
            print(f"F1 Score:  {class_metrics['f1_score']*100:.2f}%")
    
    return report 