import json
import datetime
from config import RESULT_DIR, CROP_PROMPT_CONFIGS, COUNT_PROMPT_CONFIGS, MODELS
from utils.helpers import get_summary_report_path

def generate_summary_report(all_reports, experiment_types):
    """生成汇总报告"""
    summary_report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "total_tests": len(all_reports),
        "models_tested": MODELS,
        "experiment_types": list(experiment_types.keys()),
        "prompt_configs": {
            "crop": CROP_PROMPT_CONFIGS,
            "count": COUNT_PROMPT_CONFIGS
        },
        "reports": all_reports
    }
    
    # 保存汇总报告
    summary_report_path = get_summary_report_path()
    with open(summary_report_path, 'w') as f:
        json.dump(summary_report, f, indent=4)
    
    print("\n所有模型、数据集和提示词配置测试完成!")
    print(f"详细报告已保存到 {summary_report_path}")
    
    return summary_report_path 