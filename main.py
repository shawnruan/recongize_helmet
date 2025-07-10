import os
import argparse
import numpy as np
import copy
from config import (
    MODELS, EXPERIMENT_TYPES
)
from utils.helpers import ensure_result_dir
from utils.processor import process_dataset
from utils.reporter import generate_summary_report

def calculate_average_metrics(all_runs_reports, experiment_types):
    """计算多次运行的平均量化指标"""
    print(f"\n=== 计算 {len(all_runs_reports)} 次运行的平均指标 ===")
    
    # 按实验类型、模型、数据集、类别等分组
    grouped_reports = {}
    
    for run_idx, reports in enumerate(all_runs_reports):
        print(f"处理第 {run_idx + 1} 次运行的结果...")
        
        for report in reports:
            # 创建唯一键来分组相同配置的报告
            key = (
                report['dataset'],
                report.get('category'),
                report['model'],
                report['prompt_file'],
                report['experiment_type']
            )
            
            if key not in grouped_reports:
                grouped_reports[key] = []
            grouped_reports[key].append(report)
    
    # 计算每组的平均指标
    averaged_reports = []
    
    for key, reports in grouped_reports.items():
        if not reports:
            continue
            
        # 取第一个报告作为模板
        base_report = copy.deepcopy(reports[0])
        experiment_type = base_report['experiment_type']
        
        # 收集所有指标数据
        all_metrics = [report['metrics'] for report in reports]
        
        # 计算平均指标
        avg_metrics = {}
        
        if experiment_type in ["crop", "binary"]:
            # 对于分类任务，计算精确度、召回率等的平均值
            metric_keys = ['accuracy', 'precision', 'recall', 'f1_score']
            if experiment_type == "crop":
                metric_keys.extend(['head_precision', 'head_recall', 'head_f1', 
                                  'helmet_precision', 'helmet_recall', 'helmet_f1', 'f1_macro'])
            
            for metric in metric_keys:
                values = [m.get(metric, 0) for m in all_metrics if metric in m]
                if values:
                    avg_metrics[metric] = np.mean(values)
                    avg_metrics[f'{metric}_std'] = np.std(values)
        else:
            # 对于计数任务，计算MAE、RMSE等的平均值
            metric_keys = ['mae', 'rmse', 'total_count_accuracy']
            for metric in metric_keys:
                values = [m.get(metric, 0) for m in all_metrics if metric in m]
                if values:
                    avg_metrics[metric] = np.mean(values)
                    avg_metrics[f'{metric}_std'] = np.std(values)
        
        # 计算平均时间
        all_timing = [report['timing'] for report in reports]
        avg_timing = {}
        timing_keys = ['total_time', 'total_inference_time', 'average_inference_time']
        for timing_key in timing_keys:
            values = [t.get(timing_key, 0) for t in all_timing if timing_key in t]
            if values:
                avg_timing[timing_key] = np.mean(values)
                avg_timing[f'{timing_key}_std'] = np.std(values)
        
        successful_predictions = [t.get('successful_predictions', 0) for t in all_timing]
        avg_timing['successful_predictions'] = np.mean(successful_predictions)
        
        # 更新报告
        base_report['metrics'] = avg_metrics
        base_report['timing'] = avg_timing
        base_report['total_samples'] = int(np.mean([r.get('total_samples', 0) for r in reports]))
        base_report['run_count'] = len(reports)
        base_report['run_statistics'] = {
            'mean_calculated_from': len(reports),
            'individual_run_metrics': [r['metrics'] for r in reports]
        }
        
        # 移除results字段（太大了）
        if 'results' in base_report:
            del base_report['results']
            
        averaged_reports.append(base_report)
    
    return averaged_reports

def print_average_summary(averaged_reports):
    """打印平均结果摘要"""
    print(f"\n=== 多次运行平均结果摘要 ===")
    
    for report in averaged_reports:
        dataset_name = os.path.basename(report['dataset'])
        category = report.get('category', 'full_image')
        model = report['model']
        exp_type = report['experiment_type']
        run_count = report['run_count']
        
        print(f"\n{dataset_name} - {category} ({model}, {exp_type})")
        print(f"运行次数: {run_count}")
        
        metrics = report['metrics']
        
        if exp_type in ["crop", "binary"]:
            print(f"Accuracy:  {metrics.get('accuracy', 0)*100:.2f}% ± {metrics.get('accuracy_std', 0)*100:.2f}%")
            print(f"Precision: {metrics.get('precision', 0)*100:.2f}% ± {metrics.get('precision_std', 0)*100:.2f}%")
            print(f"Recall:    {metrics.get('recall', 0)*100:.2f}% ± {metrics.get('recall_std', 0)*100:.2f}%")
            print(f"F1 Score:  {metrics.get('f1_score', 0)*100:.2f}% ± {metrics.get('f1_score_std', 0)*100:.2f}%")
            
            if exp_type == "crop" and 'f1_macro' in metrics:
                print(f"F1 Macro:  {metrics.get('f1_macro', 0)*100:.2f}% ± {metrics.get('f1_macro_std', 0)*100:.2f}%")
        else:
            print(f"MAE:  {metrics.get('mae', 0):.3f} ± {metrics.get('mae_std', 0):.3f}")
            print(f"RMSE: {metrics.get('rmse', 0):.3f} ± {metrics.get('rmse_std', 0):.3f}")
        
        timing = report['timing']
        avg_time = timing.get('average_inference_time', 0)
        avg_time_std = timing.get('average_inference_time_std', 0)
        print(f"平均推理时间: {avg_time:.3f} ± {avg_time_std:.3f} 秒/张")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='运行模型评估')
    parser.add_argument('--runs', '-r', type=int, default=1, 
                       help='运行次数 (默认: 1)')
    
    args = parser.parse_args()
    runs = args.runs
    
    if runs < 1:
        print("错误: 运行次数必须大于等于1")
        return
    
    print(f"开始进行 {runs} 次模型评估...")
    
    # 确保结果目录存在
    ensure_result_dir()
    
    # 存储所有运行的结果
    all_runs_reports = []
    
    # 运行指定次数
    for run_idx in range(runs):
        print(f"\n{'='*50}")
        print(f"开始第 {run_idx + 1}/{runs} 次运行")
        print(f"{'='*50}")
        
        current_run_reports = []
        
        # 处理每个实验类型
        for exp_type, exp_config in EXPERIMENT_TYPES.items():
            print(f"\n开始{exp_type}类型实验")
            
            # 处理每个模型
            for model in MODELS:
                print(f"\n开始测试模型: {model}")
                
                # 处理每个提示词配置
                for prompt_config in exp_config["prompts"]:
                    prompt_name = os.path.splitext(os.path.basename(prompt_config))[0]
                    print(f"\n使用提示词配置: {prompt_name}")
                    
                    # 处理每个数据集
                    for dataset in exp_config["datasets"]:
                        if exp_type in ["crop", "binary"]:
                            # 对于裁剪图片实验和二分类实验，需要处理每个类别
                            for category in exp_config["categories"]:
                                report = process_dataset(
                                    dataset, 
                                    category,
                                    f"validation_{exp_type}_{dataset.split('/')[-1].split('_')[0]}_run{run_idx+1}",
                                    prompt_config,
                                    model,
                                    exp_type
                                )
                                report["prompt_config"] = prompt_name
                                report["run_index"] = run_idx + 1
                                current_run_reports.append(report)
                        else:
                            # 对于完整图片实验，不需要处理类别
                            report = process_dataset(
                                dataset,
                                None,
                                f"validation_{exp_type}_{dataset.split('/')[-1].split('_')[0]}_run{run_idx+1}",
                                prompt_config,
                                model,
                                exp_type
                            )
                            report["prompt_config"] = prompt_name
                            report["run_index"] = run_idx + 1
                            current_run_reports.append(report)
        
        all_runs_reports.append(current_run_reports)
        
        print(f"\n第 {run_idx + 1} 次运行完成，共处理了 {len(current_run_reports)} 个测试配置")
    
    # 如果运行了多次，计算平均指标
    if runs > 1:
        print(f"\n{'='*60}")
        print(f"所有 {runs} 次运行完成，开始计算平均指标...")
        print(f"{'='*60}")
        
        # 计算平均指标
        averaged_reports = calculate_average_metrics(all_runs_reports, EXPERIMENT_TYPES)
        
        # 打印平均结果摘要
        print_average_summary(averaged_reports)
        
        # 生成包含平均指标的汇总报告
        generate_summary_report(averaged_reports, EXPERIMENT_TYPES)
        
        print(f"\n多次运行评估完成！")
        print(f"总共运行了 {runs} 次，每次运行了 {len(all_runs_reports[0])} 个测试配置")
        print(f"平均指标已计算并保存到汇总报告中")
        
    else:
        # 单次运行，使用原有逻辑
        generate_summary_report(all_runs_reports[0], EXPERIMENT_TYPES)

if __name__ == "__main__":
    main()