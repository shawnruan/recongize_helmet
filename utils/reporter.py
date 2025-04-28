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
    
    return summary_report_path 