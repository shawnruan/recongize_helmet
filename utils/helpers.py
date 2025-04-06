import os
from config import RESULT_DIR

def clean_model_name(model_name):
    """清理模型名称，替换不允许在文件名中使用的字符"""
    return model_name.replace(':', '_')

def ensure_result_dir():
    """确保结果目录存在"""
    os.makedirs(RESULT_DIR, exist_ok=True)

def get_output_file_path(output_prefix, model, category, experiment_type, prompt_file=None):
    """获取输出文件路径
    
    Args:
        output_prefix: 输出文件前缀
        model: 模型名称
        category: 分类标识符（crop实验为类别名，count实验为数据集名）
        experiment_type: 实验类型
        prompt_file: 提示词文件路径
        
    Returns:
        完整的输出文件路径
    """
    clean_model = clean_model_name(model)
    
    # 提取提示词名称
    prompt_name = ""
    if prompt_file:
        prompt_basename = os.path.basename(prompt_file)
        prompt_name = prompt_basename.replace('.md', '')
    
    if experiment_type == "count":
        # count实验使用数据集名称作为标识符
        return os.path.join(RESULT_DIR, f"{output_prefix}_{clean_model}_{prompt_name}_{category}_report.json")
    else:
        # crop实验使用类别名作为标识符
        return os.path.join(RESULT_DIR, f"{output_prefix}_{clean_model}_{prompt_name}_{category}_report.json")

def get_summary_report_path():
    """获取汇总报告路径"""
    return os.path.join(RESULT_DIR, "validation_summary_report.json") 