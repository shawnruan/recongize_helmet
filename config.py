# API配置
API_URL = "http://localhost:11434/api/generate"

# Transformer 模型配置
TRANSFORMER_MODEL_PATH = "models/minicpm-v"  # 本地模型路径，如果不存在则使用 HuggingFace ID
TRANSFORMER_MODELS = ["Qwen/Qwen-VL-Chat", "TencentARC/minicpm-v-2"]  # HuggingFace 模型ID

# LLM Studio 配置
LLM_STUDIO_API_URL = "http://localhost:8000/v1/chat/completions"
LLM_STUDIO_API_KEY = None  # 如果需要
LLM_STUDIO_MODELS = ["vllm-model"]

# 模型配置
MODELS = [
    #"minicpm-o",
    "gemma3:27b",
    "gemma3:12b",
    "minicpm-v"
    #"qwen-7b"
]

# 提示词配置文件
CROP_PROMPT_CONFIGS = [
    "prompts/test-prompts.md",
    "prompts/test-prompts-en.md"
]

COUNT_PROMPT_CONFIGS = [
    "prompts/count-prompts.md",
    "prompts/detect-prompts.md"
]

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
    }
} 