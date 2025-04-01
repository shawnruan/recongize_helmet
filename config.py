# API配置
API_URL = "http://localhost:11434/api/generate"

# 结果保存目录
RESULT_DIR = "result"

# 模型配置
MODELS = [
    "minicpm-o",
    "minicpm-v",
    "qwen-7b"
]

# 提示词配置文件
PROMPT_CONFIGS = [
    "prompts/test-prompts.md",
    "prompts/detailed-prompts.md",
    "prompts/bilingual-prompts.md",
    "prompts/safety-focused-prompts.md"
]

# 数据集配置
DATASETS = [
    "dataset/helmet_sample_output_crops",
    "dataset/lng_output_crops"
]

# 类别配置
CATEGORIES = ["person", "head_helmet"] 