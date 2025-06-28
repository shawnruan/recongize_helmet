import json
import datetime
import copy
import os
from config import RESULT_DIR, CROP_PROMPT_CONFIGS, COUNT_PROMPT_CONFIGS, BINARY_PROMPT_CONFIGS, MODELS, BINARY_THRESHOLD
from utils.helpers import get_summary_report_path
from utils.visualization import ensure_picture_dir

def generate_summary_report(all_reports, experiment_types):
    """生成汇总报告，但移除每个报告中的results字段以减小文件大小"""
    # 确保图片目录存在
    ensure_picture_dir()
    
    # 深拷贝报告列表，避免修改原始数据
    summary_reports = []
    total_inference_time = 0
    total_samples = 0
    
    # 记录所有二分类实验的分布图
    distribution_plots = []
    
    for report in all_reports:
        # 创建报告的副本并移除 results 字段
        summary_report = copy.deepcopy(report)
        
        # 提取时间信息
        if 'timing' in summary_report:
            total_inference_time += summary_report['timing'].get('total_inference_time', 0)
            total_samples += summary_report['timing'].get('successful_predictions', 0)
        
        # 记录分布图信息
        if 'distribution_plots' in summary_report:
            dist_info = {
                'dataset': summary_report.get('dataset', ''),
                'category': summary_report.get('category', ''),
                'model': summary_report.get('model', ''),
                'prompt_file': summary_report.get('prompt_file', ''),
                'plots': summary_report['distribution_plots']
            }
            distribution_plots.append(dist_info)
        
        # 移除 results 字段以减小文件大小
        if 'results' in summary_report:
            del summary_report['results']
            
        summary_reports.append(summary_report)
    
    # 计算平均推理时间
    avg_inference_time = total_inference_time / total_samples if total_samples > 0 else 0
    
    # 生成F1_macro汇总分析（仅针对crop实验）
    f1_macro_summary = generate_f1_macro_summary(all_reports)
    
    # 创建汇总报告
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total_tests": len(all_reports),
        "models_tested": MODELS,
        "experiment_types": list(experiment_types.keys()),
        "prompt_configs": {
            "crop": CROP_PROMPT_CONFIGS,
            "count": COUNT_PROMPT_CONFIGS,
            "binary": BINARY_PROMPT_CONFIGS
        },
        "binary_threshold": BINARY_THRESHOLD,
        "timing_summary": {
            "total_inference_time": round(total_inference_time, 3),
            "total_samples": total_samples,
            "average_inference_time": round(avg_inference_time, 3)
        },
        "f1_macro_summary": f1_macro_summary,
        "distribution_plots": distribution_plots if distribution_plots else None,
        "reports": summary_reports  # 使用不含 results 字段的报告列表
    }
    
    # 保存汇总报告
    summary_report_path = get_summary_report_path()
    with open(summary_report_path, 'w') as f:
        json.dump(report, f, indent=4)
    
    print("\n所有模型、数据集和提示词配置测试完成!")
    print(f"详细报告已保存到 {summary_report_path}")
    if distribution_plots:
        print(f"分布图已保存到 {os.path.join(RESULT_DIR, 'picture')}")
    print(f"总推理时间: {total_inference_time:.3f}秒")
    print(f"总样本数: {total_samples}")
    print(f"平均推理时间: {avg_inference_time:.3f}秒/张")
    
    # 打印F1_macro汇总分析
    if f1_macro_summary:
        print_f1_macro_summary(f1_macro_summary)
    
    return summary_report_path

def generate_f1_macro_summary(all_reports):
    """生成F1_macro汇总分析"""
    # 只处理crop实验的报告
    crop_reports = [r for r in all_reports if r.get('experiment_type') == 'crop']
    
    if not crop_reports:
        return None
    
    # 数据结构：{dataset_name: [f1_macro_values]}
    dataset_scores = {}
    # 数据结构：{model: [f1_macro_values]}
    model_scores = {}
    # 数据结构：{prompt_name: [f1_macro_values]}
    prompt_scores = {}
    # 数据结构：{prompt_name: {dataset_name: [f1_macro_values]}}
    prompt_dataset_scores = {}
    # 数据结构：{model: {dataset_name: [f1_macro_values]}}
    model_dataset_scores = {}
    # 数据结构：{model: {prompt_name: [f1_macro_values]}}
    model_prompt_scores = {}
    
    for report in crop_reports:
        # 获取基本信息
        dataset_base = os.path.basename(report['dataset'])
        category = report.get('category', '')
        model = report['model']
        prompt_file = report.get('prompt_file', '')
        
        # 确定数据集名称
        if 'helmet_sample' in dataset_base or 'sample' in dataset_base:
            dataset_prefix = 'sample'
        elif 'lng' in dataset_base:
            dataset_prefix = 'lng'
        else:
            dataset_prefix = dataset_base
        
        dataset_name = f"{dataset_prefix}_{category}"
        
        # 确定 prompt 名称
        prompt_name = os.path.basename(prompt_file).replace('.md', '') if prompt_file else 'unknown'
        
        # 获取F1_macro值
        f1_macro = report.get('metrics', {}).get('f1_macro', 0)
        
        # 存储数据集分数
        if dataset_name not in dataset_scores:
            dataset_scores[dataset_name] = []
        dataset_scores[dataset_name].append(f1_macro)
        
        # 存储模型分数
        if model not in model_scores:
            model_scores[model] = []
        model_scores[model].append(f1_macro)
        
        # 存储 prompt 分数
        if prompt_name not in prompt_scores:
            prompt_scores[prompt_name] = []
        prompt_scores[prompt_name].append(f1_macro)
        
        # 存储 prompt-dataset 分数
        if prompt_name not in prompt_dataset_scores:
            prompt_dataset_scores[prompt_name] = {}
        if dataset_name not in prompt_dataset_scores[prompt_name]:
            prompt_dataset_scores[prompt_name][dataset_name] = []
        prompt_dataset_scores[prompt_name][dataset_name].append(f1_macro)
        
        # 存储 model-dataset 分数
        if model not in model_dataset_scores:
            model_dataset_scores[model] = {}
        if dataset_name not in model_dataset_scores[model]:
            model_dataset_scores[model][dataset_name] = []
        model_dataset_scores[model][dataset_name].append(f1_macro)
        
        # 存储 model-prompt 分数
        if model not in model_prompt_scores:
            model_prompt_scores[model] = {}
        if prompt_name not in model_prompt_scores[model]:
            model_prompt_scores[model][prompt_name] = []
        model_prompt_scores[model][prompt_name].append(f1_macro)
    
    # 计算平均值
    dataset_averages = {}
    for dataset, scores in dataset_scores.items():
        dataset_averages[dataset] = {
            'average': sum(scores) / len(scores) if scores else 0
        }
    
    model_averages = {}
    for model, scores in model_scores.items():
        model_averages[model] = {
            'average': sum(scores) / len(scores) if scores else 0
        }
    
    prompt_averages = {}
    for prompt, scores in prompt_scores.items():
        prompt_averages[prompt] = {
            'average': sum(scores) / len(scores) if scores else 0
        }
    
    # 计算 prompt-dataset 平均值
    prompt_dataset_averages = {}
    for prompt, datasets in prompt_dataset_scores.items():
        prompt_dataset_averages[prompt] = {}
        for dataset, scores in datasets.items():
            prompt_dataset_averages[prompt][dataset] = {
                'average': sum(scores) / len(scores) if scores else 0
            }
    
    # 计算 model-dataset 平均值
    model_dataset_averages = {}
    for model, datasets in model_dataset_scores.items():
        model_dataset_averages[model] = {}
        for dataset, scores in datasets.items():
            model_dataset_averages[model][dataset] = {
                'average': sum(scores) / len(scores) if scores else 0
            }
    
    # 计算 model-prompt 平均值
    model_prompt_averages = {}
    for model, prompts in model_prompt_scores.items():
        model_prompt_averages[model] = {}
        for prompt, scores in prompts.items():
            model_prompt_averages[model][prompt] = {
                'average': sum(scores) / len(scores) if scores else 0
            }
    
    return {
        'dataset_scores': dataset_averages,
        'model_scores': model_averages,
        'prompt_scores': prompt_averages,
        'prompt_dataset_scores': prompt_dataset_averages,
        'model_dataset_scores': model_dataset_averages,
        'model_prompt_scores': model_prompt_averages
    }

def print_f1_macro_summary(f1_macro_summary):
    """打印F1_macro汇总分析"""
    if not f1_macro_summary:
        return
    
    print("\n" + "="*80)
    print("### Model Performance Summary - Head Positive")
    print("="*80)
    
    # 打印数据集F1_macro分数表格
    print("\n#### Final F1 Macro Scores by Dataset")
    print()
    print("| Dataset            | F1_Macro |")
    print("| ------------------ | -------- |")
    
    dataset_scores = f1_macro_summary['dataset_scores']
    
    # 按数据集名称排序
    sorted_datasets = sorted(dataset_scores.keys())
    for dataset in sorted_datasets:
        scores = dataset_scores[dataset]
        avg_score = scores.get('average', 0) * 100
        
        print(f"| {dataset:<18} | {avg_score:>7.2f}% |")
    
    # 打印模型最终分数表格
    print("\n#### Model Final Scores (Average across all datasets)")
    print()
    print("| Model           | F1_Macro |")
    print("| --------------- | -------- |")
    
    model_scores = f1_macro_summary['model_scores']
    
    # 按模型名称排序
    sorted_models = sorted(model_scores.keys())
    for model in sorted_models:
        scores = model_scores[model]
        avg_score = scores.get('average', 0) * 100
        
        print(f"| {model:<15} | {avg_score:>7.2f}% |")
    
    # 打印 prompt 最终分数表格
    if 'prompt_scores' in f1_macro_summary:
        print("\n#### Prompt Final Scores (Average across all datasets and models)")
        print()
        print("| Prompt          | F1_Macro |")
        print("| --------------- | -------- |")
        
        prompt_scores = f1_macro_summary['prompt_scores']
        
        # 按 prompt 名称排序
        sorted_prompts = sorted(prompt_scores.keys())
        for prompt in sorted_prompts:
            scores = prompt_scores[prompt]
            avg_score = scores.get('average', 0) * 100
            
            print(f"| {prompt:<15} | {avg_score:>7.2f}% |")
    
    # 新增：模型-数据集详细性能矩阵
    if 'model_dataset_scores' in f1_macro_summary:
        print("\n#### Model Performance by Dataset (Detailed)")
        print()
        
        model_dataset_scores = f1_macro_summary['model_dataset_scores']
        
        # 获取所有数据集名称并排序
        all_datasets = set()
        for model_data in model_dataset_scores.values():
            all_datasets.update(model_data.keys())
        sorted_datasets = sorted(all_datasets)
        
        # 创建表头
        header = "| Model           |"
        separator = "| --------------- |"
        for dataset in sorted_datasets:
            dataset_short = dataset.replace('_', '_')[:12]  # 缩短列名
            header += f" {dataset_short:<12} |"
            separator += " ------------ |"
        
        print(header)
        print(separator)
        
        # 按模型名称排序并打印每行
        sorted_models = sorted(model_dataset_scores.keys())
        for model in sorted_models:
            datasets = model_dataset_scores[model]
            row = f"| {model:<15} |"
            
            for dataset in sorted_datasets:
                if dataset in datasets:
                    avg_score = datasets[dataset].get('average', 0) * 100
                    row += f" {avg_score:>10.2f}% |"
                else:
                    row += "        N/A |"
            
            print(row)
    
    # 新增：模型-提示词详细性能矩阵
    if 'model_prompt_scores' in f1_macro_summary:
        print("\n#### Model Performance by Prompt (Detailed)")
        print()
        
        model_prompt_scores = f1_macro_summary['model_prompt_scores']
        
        # 获取所有提示词名称并排序
        all_prompts = set()
        for model_data in model_prompt_scores.values():
            all_prompts.update(model_data.keys())
        sorted_prompts = sorted(all_prompts)
        
        # 创建表头
        header = "| Model           |"
        separator = "| --------------- |"
        for prompt in sorted_prompts:
            prompt_short = prompt.replace('easy-prompts-', '')[:10]
            header += f" {prompt_short:<10} |"
            separator += " ---------- |"
        
        print(header)
        print(separator)
        
        # 按模型名称排序并打印每行
        sorted_models = sorted(model_prompt_scores.keys())
        for model in sorted_models:
            prompts = model_prompt_scores[model]
            row = f"| {model:<15} |"
            
            for prompt in sorted_prompts:
                if prompt in prompts:
                    avg_score = prompts[prompt].get('average', 0) * 100
                    row += f" {avg_score:>8.2f}% |"
                else:
                    row += "      N/A |"
            
            print(row)
    
    # 打印 prompt-dataset 详细分数表格
    if 'prompt_dataset_scores' in f1_macro_summary:
        print("\n#### Prompt Performance by Dataset")
        print()
        
        prompt_dataset_scores = f1_macro_summary['prompt_dataset_scores']
        
        # 获取所有数据集名称并排序
        all_datasets = set()
        for prompt_data in prompt_dataset_scores.values():
            all_datasets.update(prompt_data.keys())
        sorted_datasets = sorted(all_datasets)
        
        # 创建表头
        header = "| Prompt          |"
        separator = "| --------------- |"
        for dataset in sorted_datasets:
            dataset_short = dataset.replace('_', '_')[:10]
            header += f" {dataset_short:<10} |"
            separator += " ---------- |"
        
        print(header)
        print(separator)
        
        # 按 prompt 名称排序并打印每行
        sorted_prompts = sorted(prompt_dataset_scores.keys())
        for prompt in sorted_prompts:
            datasets = prompt_dataset_scores[prompt]
            row = f"| {prompt:<15} |"
            
            for dataset in sorted_datasets:
                if dataset in datasets:
                    avg_score = datasets[dataset].get('average', 0) * 100
                    row += f" {avg_score:>8.2f}% |"
                else:
                    row += "      N/A |"
            
            print(row)
    
    print("\n" + "="*80) 