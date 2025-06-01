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
    
    # 数据结构：{dataset_name: {prompt_type: [f1_macro_values]}}
    dataset_scores = {}
    # 数据结构：{model: {prompt_type: [f1_macro_values]}}
    model_scores = {}
    
    for report in crop_reports:
        # 获取基本信息
        dataset_base = os.path.basename(report['dataset'])
        category = report.get('category', '')
        model = report['model']
        prompt_file = report['prompt_file']
        
        # 确定数据集名称
        if 'helmet_sample' in dataset_base or 'sample' in dataset_base:
            dataset_prefix = 'sample'
        elif 'lng' in dataset_base:
            dataset_prefix = 'lng'
        else:
            dataset_prefix = dataset_base
        
        dataset_name = f"{dataset_prefix}_{category}"
        
        # 确定提示词类型
        if 'test-prompts-en.md' in prompt_file:
            prompt_type = 'english'
        elif 'test-prompts.md' in prompt_file:
            prompt_type = 'chinese'
        else:
            prompt_type = 'other'
        
        # 获取F1_macro值
        f1_macro = report.get('metrics', {}).get('f1_macro', 0)
        
        # 存储数据集分数
        if dataset_name not in dataset_scores:
            dataset_scores[dataset_name] = {}
        if prompt_type not in dataset_scores[dataset_name]:
            dataset_scores[dataset_name][prompt_type] = []
        dataset_scores[dataset_name][prompt_type].append(f1_macro)
        
        # 存储模型分数
        if model not in model_scores:
            model_scores[model] = {}
        if prompt_type not in model_scores[model]:
            model_scores[model][prompt_type] = []
        model_scores[model][prompt_type].append(f1_macro)
    
    # 计算平均值
    dataset_averages = {}
    for dataset, scores in dataset_scores.items():
        dataset_averages[dataset] = {}
        for prompt_type, values in scores.items():
            dataset_averages[dataset][prompt_type] = sum(values) / len(values) if values else 0
        
        # 计算数据集总平均值
        all_values = []
        for prompt_type in ['chinese', 'english']:
            if prompt_type in dataset_averages[dataset]:
                all_values.append(dataset_averages[dataset][prompt_type])
        dataset_averages[dataset]['average'] = sum(all_values) / len(all_values) if all_values else 0
    
    model_averages = {}
    for model, scores in model_scores.items():
        model_averages[model] = {}
        for prompt_type, values in scores.items():
            model_averages[model][prompt_type] = sum(values) / len(values) if values else 0
    
    return {
        'dataset_scores': dataset_averages,
        'model_scores': model_averages
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
    print("| Dataset            | Chinese Prompts | English Prompts | Dataset Average |")
    print("| ------------------ | --------------- | --------------- | --------------- |")
    
    dataset_scores = f1_macro_summary['dataset_scores']
    
    # 按数据集名称排序
    sorted_datasets = sorted(dataset_scores.keys())
    for dataset in sorted_datasets:
        scores = dataset_scores[dataset]
        chinese_score = scores.get('chinese', 0) * 100
        english_score = scores.get('english', 0) * 100
        avg_score = scores.get('average', 0) * 100
        
        print(f"| {dataset:<18} | {chinese_score:>13.2f}% | {english_score:>13.2f}% | {avg_score:>13.2f}% |")
    
    # 打印模型最终分数表格
    print("\n#### Model Final Scores (Average across all datasets and prompts)")
    print()
    print("| Model           | Chinese F1_Macro | English F1_Macro |")
    print("| --------------- | ---------------- | ---------------- |")
    
    model_scores = f1_macro_summary['model_scores']
    
    # 按模型名称排序
    sorted_models = sorted(model_scores.keys())
    for model in sorted_models:
        scores = model_scores[model]
        chinese_score = scores.get('chinese', 0) * 100
        english_score = scores.get('english', 0) * 100
        
        # 添加最高分标记
        chinese_mark = "**" if chinese_score == max([model_scores[m].get('chinese', 0) * 100 for m in model_scores]) else ""
        english_mark = "**" if english_score == max([model_scores[m].get('english', 0) * 100 for m in model_scores]) else ""
        
        chinese_display = f"{chinese_mark}{chinese_score:.2f}%{chinese_mark}" if chinese_mark else f"{chinese_score:.2f}%"
        english_display = f"{english_mark}{english_score:.2f}%{english_mark}" if english_mark else f"{english_score:.2f}%"
        
        print(f"| {model:<15} | {chinese_display:>16} | {english_display:>16} |")
    
    print("\n" + "="*80) 