import json
import datetime
import copy
from config import RESULT_DIR, CROP_PROMPT_CONFIGS, COUNT_PROMPT_CONFIGS, MODELS
from utils.helpers import get_summary_report_path

def generate_summary_report(all_reports, experiment_types):
    """生成汇总报告，但移除每个报告中的results字段以减小文件大小"""
    # 深拷贝报告列表，避免修改原始数据
    summary_reports = []
    for report in all_reports:
        # 创建报告的副本并移除 results 字段
        summary_report = copy.deepcopy(report)
        if 'results' in summary_report:
            del summary_report['results']
        summary_reports.append(summary_report)
    
    # 创建汇总报告
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total_tests": len(all_reports),
        "models_tested": MODELS,
        "experiment_types": list(experiment_types.keys()),
        "prompt_configs": {
            "crop": CROP_PROMPT_CONFIGS,
            "count": COUNT_PROMPT_CONFIGS
        },
        "reports": summary_reports  # 使用不含 results 字段的报告列表
    }
    
    # 保存汇总报告
    summary_report_path = get_summary_report_path()
    with open(summary_report_path, 'w') as f:
        json.dump(report, f, indent=4)
    
    print("\n所有模型、数据集和提示词配置测试完成!")
    print(f"详细报告已保存到 {summary_report_path}")
    
    return summary_report_path 