# API配置
API_URL = "http://localhost:11434/api/generate"

# 模型配置
MODELS = [
    # "deepseek-janus",
    # "qwen2.5-vl-32b",
    # "minicpm-o",
    "minicpm-v",
    # "deepseek-r1:7b",
    # "deepseek-r1:32b",
    # "gemma3:27b",
    #"gemma3:12b"
    #"qwen-7b",
    #"qwen2.5-vl-72b",
    
]

# 提示词配置文件
CROP_PROMPT_CONFIGS = [
    #"prompts/test-prompts.md",
    # "prompts/test-prompts-en.md"
]

COUNT_PROMPT_CONFIGS = [
    # "prompts/count-prompts.md",
    # "prompts/detect-prompts.md"
]

# 二分类实验的提示词配置
BINARY_PROMPT_CONFIGS = [
    "prompts/helmet-probability-prompt.md",
    #"prompts/helmet-detailed-scoring.md"
]

# 二分类实验的阈值设置
BINARY_THRESHOLD = 0.6

# 裁剪图片数据集配置
DATASETS = [
    "dataset/helmet_sample_output_crops",
    "dataset/lng_output_crops"
]

# 完整图片数据集配置
FULL_IMAGE_DATASETS = [
    "dataset/HELMET_SAMPLES_80/obj_train_data",
    "dataset/LNG_DATASET_SAMPLES_80/lng_train_data"
]

# 类别配置
CATEGORIES = ["person", "head_helmet"]

# 结果目录
RESULT_DIR = "result"

# 实验类型配置
EXPERIMENT_TYPES = {
    "crop": {  # 裁剪图片实验
        "datasets": DATASETS,
        "categories": CATEGORIES,
        "prompts": CROP_PROMPT_CONFIGS  # 使用裁剪图片专用提示词
    },
    "count": {  # 数量统计实验
        "datasets": FULL_IMAGE_DATASETS,
        "prompts": COUNT_PROMPT_CONFIGS  # 使用数量统计专用提示词
    },
    "binary": {  # 二分类实验 
        "datasets": DATASETS,
        "categories": CATEGORIES,
        "prompts": BINARY_PROMPT_CONFIGS,  # 使用二分类专用提示词
        "threshold": BINARY_THRESHOLD  # 分类阈值
    }
} 