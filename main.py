import os
from config import (
    MODELS, EXPERIMENT_TYPES
)
from utils.helpers import ensure_result_dir
from utils.processor import process_dataset
from utils.reporter import generate_summary_report

def main():
    """主函数"""
    # 确保结果目录存在
    ensure_result_dir()
    
    all_reports = []
    
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
                    if exp_type == "crop":
                        # 对于裁剪图片实验，需要处理每个类别
                        for category in exp_config["categories"]:
                            report = process_dataset(
                                dataset, 
                                category,
                                f"validation_{exp_type}_{dataset.split('/')[-1].split('_')[0]}",  # 使用数据集前缀作为输出文件名
                                prompt_config,
                                model,
                                exp_type
                            )
                            report["prompt_config"] = prompt_name
                            all_reports.append(report)
                    else:
                        # 对于完整图片实验，不需要处理类别
                        report = process_dataset(
                            dataset,
                            None,
                            f"validation_{exp_type}_{dataset.split('/')[-1].split('_')[0]}",  # 使用数据集前缀作为输出文件名
                            prompt_config,
                            model,
                            exp_type
                        )
                        report["prompt_config"] = prompt_name
                        all_reports.append(report)
    
    # 生成汇总报告
    generate_summary_report(all_reports, EXPERIMENT_TYPES)

if __name__ == "__main__":
    main()