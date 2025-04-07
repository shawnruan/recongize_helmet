# Helmet Detection Evaluation System

This project implements a safety helmet wearing detection and statistics system based on vision large models, supporting evaluation of multiple models, multiple prompt configurations, and multiple experiment types.

## Project Features

- Support for multiple vision model evaluations (Ollama API, Transformer, GGUF)
- Two evaluation tasks: cropped image object recognition (crop) and full image counting (count)
- Multiple prompt configurations, supporting both Chinese and English
- Comprehensive evaluation metrics calculation
- Results saved in the `result` directory

## Model Performance Comparison

### Cropped Image Object Recognition (Crop) Task

#### Chinese Prompts (test-prompts.md)

| Model | Dataset | Category | Accuracy | Precision | Recall | F1 Score |
|------|--------|------|--------|--------|--------|--------|
| gemma3:27b | helmet_sample | person | 69.77% | 63.13% | 96.15% | 76.22% |
| gemma3:27b | helmet_sample | head_helmet | 92.28% | 96.69% | 93.09% | 94.85% |
| gemma3:27b | lng_output | person | 75.13% | 78.72% | 86.72% | 82.53% |
| gemma3:27b | lng_output | head_helmet | 62.37% | 86.73% | 64.05% | 73.68% |
| gemma3:12b | helmet_sample | person | 68.22% | 61.88% | 96.15% | 75.30% |
| gemma3:12b | helmet_sample | head_helmet | 91.87% | 96.15% | 93.09% | 94.59% |
| gemma3:12b | lng_output | person | 77.25% | 78.52% | 91.41% | 84.48% |
| gemma3:12b | lng_output | head_helmet | 72.58% | 89.23% | 75.82% | 81.98% |
| minicpm-v | helmet_sample | person | 69.38% | 63.35% | 93.08% | 75.39% |
| minicpm-v | helmet_sample | head_helmet | 91.87% | 96.15% | 93.09% | 94.59% |
| minicpm-v | lng_output | person | 71.43% | 80.33% | 76.56% | 78.40% |
| minicpm-v | lng_output | head_helmet | 58.60% | 90.43% | 55.56% | 68.83% |

#### English Prompts (test-prompts-en.md)

| Model | Dataset | Category | Accuracy | Precision | Recall | F1 Score |
|------|--------|------|--------|--------|--------|--------|
| gemma3:27b | helmet_sample | person | 70.54% | 64.84% | 90.77% | 75.64% |
| gemma3:27b | helmet_sample | head_helmet | 88.62% | 99.38% | 85.64% | 92.00% |
| gemma3:27b | lng_output | person | 69.31% | 80.70% | 71.88% | 76.03% |
| gemma3:27b | lng_output | head_helmet | 54.30% | 95.95% | 46.41% | 62.56% |
| gemma3:12b | helmet_sample | person | 44.57% | 40.58% | 21.54% | 28.14% |
| gemma3:12b | helmet_sample | head_helmet | 70.33% | 90.78% | 68.09% | 77.81% |
| gemma3:12b | lng_output | person | 67.20% | 74.63% | 78.13% | 76.34% |
| gemma3:12b | lng_output | head_helmet | 53.76% | 84.54% | 53.59% | 65.60% |
| minicpm-v | helmet_sample | person | 71.71% | 65.75% | 91.54% | 76.53% |
| minicpm-v | helmet_sample | head_helmet | 89.43% | 100.00% | 86.17% | 92.57% |
| minicpm-v | lng_output | person | 66.14% | 80.19% | 66.41% | 72.65% |
| minicpm-v | lng_output | head_helmet | 36.56% | 100.00% | 22.88% | 37.23% |

### Full Image Counting (Count) Task

#### count-prompts.md

| Model | Dataset | Category | Accuracy | Precision | Recall | F1 Score |
|------|--------|------|--------|--------|--------|--------|
| gemma3:27b | HELMET_SAMPLES_80 | head | 48.60% | 51.49% | 89.66% | 65.41% |
| gemma3:27b | HELMET_SAMPLES_80 | helmet | 69.15% | 91.45% | 73.94% | 81.76% |
| gemma3:27b | HELMET_SAMPLES_80 | person | 84.48% | 92.49% | 90.70% | 91.59% |
| gemma3:27b | HELMET_SAMPLES_80 | alert | 50.00% | 50.88% | 96.67% | 66.67% |
| gemma3:27b | LNG_DATASET_SAMPLES_80 | head | 33.33% | 41.18% | 63.64% | 50.00% |
| gemma3:27b | LNG_DATASET_SAMPLES_80 | helmet | 46.70% | 67.65% | 60.13% | 63.67% |
| gemma3:27b | LNG_DATASET_SAMPLES_80 | person | 56.67% | 72.73% | 71.96% | 72.34% |
| gemma3:27b | LNG_DATASET_SAMPLES_80 | alert | 36.84% | 46.67% | 63.64% | 53.85% |
| gemma3:12b | HELMET_SAMPLES_80 | head | 35.96% | 42.27% | 70.69% | 52.90% |
| gemma3:12b | HELMET_SAMPLES_80 | helmet | 44.79% | 95.56% | 45.74% | 61.87% |
| gemma3:12b | HELMET_SAMPLES_80 | person | 70.50% | 98.40% | 71.32% | 82.70% |
| gemma3:12b | HELMET_SAMPLES_80 | alert | 42.19% | 44.26% | 90.00% | 59.34% |
| gemma3:12b | LNG_DATASET_SAMPLES_80 | head | 29.31% | 40.48% | 51.52% | 45.33% |
| gemma3:12b | LNG_DATASET_SAMPLES_80 | helmet | 39.81% | 60.74% | 53.59% | 56.94% |
| gemma3:12b | LNG_DATASET_SAMPLES_80 | person | 51.24% | 70.06% | 65.61% | 67.76% |
| gemma3:12b | LNG_DATASET_SAMPLES_80 | alert | 35.42% | 53.13% | 51.52% | 52.31% |
| minicpm-v | HELMET_SAMPLES_80 | head | 36.69% | 38.64% | 87.93% | 53.68% |
| minicpm-v | HELMET_SAMPLES_80 | helmet | 81.19% | 92.13% | 87.23% | 89.62% |
| minicpm-v | HELMET_SAMPLES_80 | person | 73.09% | 77.60% | 92.64% | 84.45% |
| minicpm-v | HELMET_SAMPLES_80 | alert | 42.86% | 48.00% | 80.00% | 60.00% |
| minicpm-v | LNG_DATASET_SAMPLES_80 | head | 18.18% | 24.14% | 42.42% | 30.77% |
| minicpm-v | LNG_DATASET_SAMPLES_80 | helmet | 60.00% | 85.71% | 66.67% | 75.00% |
| minicpm-v | LNG_DATASET_SAMPLES_80 | person | 45.58% | 48.82% | 87.30% | 62.62% |
| minicpm-v | LNG_DATASET_SAMPLES_80 | alert | 26.67% | 37.21% | 48.48% | 42.11% |

#### detect-prompts.md

| Model | Dataset | Category | Accuracy | Precision | Recall | F1 Score |
|------|--------|------|--------|--------|--------|--------|
| gemma3:27b | HELMET_SAMPLES_80 | head | 51.14% | 60.00% | 77.59% | 67.67% |
| gemma3:27b | HELMET_SAMPLES_80 | helmet | 75.76% | 93.75% | 79.79% | 86.21% |
| gemma3:27b | HELMET_SAMPLES_80 | person | 86.04% | 97.02% | 88.37% | 92.49% |
| gemma3:27b | HELMET_SAMPLES_80 | alert | 53.85% | 56.00% | 93.33% | 70.00% |
| gemma3:27b | LNG_DATASET_SAMPLES_80 | head | 34.09% | 35.29% | 90.91% | 50.85% |
| gemma3:27b | LNG_DATASET_SAMPLES_80 | helmet | 45.69% | 67.16% | 58.82% | 62.72% |
| gemma3:27b | LNG_DATASET_SAMPLES_80 | person | 51.67% | 63.47% | 73.54% | 68.14% |
| gemma3:27b | LNG_DATASET_SAMPLES_80 | alert | 42.86% | 44.78% | 90.91% | 60.00% |
| gemma3:12b | HELMET_SAMPLES_80 | head | 30.28% | 33.86% | 74.14% | 46.49% |
| gemma3:12b | HELMET_SAMPLES_80 | helmet | 51.16% | 80.29% | 58.51% | 67.69% |
| gemma3:12b | HELMET_SAMPLES_80 | person | 69.48% | 81.06% | 82.95% | 81.99% |
| gemma3:12b | HELMET_SAMPLES_80 | alert | 37.97% | 37.97% | 100.00% | 55.05% |
| gemma3:12b | LNG_DATASET_SAMPLES_80 | head | 23.66% | 24.03% | 93.94% | 38.27% |
| gemma3:12b | LNG_DATASET_SAMPLES_80 | helmet | 35.28% | 38.91% | 79.08% | 52.16% |
| gemma3:12b | LNG_DATASET_SAMPLES_80 | person | 36.15% | 37.95% | 88.36% | 53.10% |
| gemma3:12b | LNG_DATASET_SAMPLES_80 | alert | 40.79% | 41.89% | 93.94% | 57.94% |
| minicpm-v | HELMET_SAMPLES_80 | head | 22.11% | 36.21% | 36.21% | 36.21% |
| minicpm-v | HELMET_SAMPLES_80 | helmet | 76.52% | 80.73% | 93.62% | 86.70% |
| minicpm-v | HELMET_SAMPLES_80 | person | 80.00% | 83.85% | 94.57% | 88.89% |
| minicpm-v | HELMET_SAMPLES_80 | alert | 25.00% | 35.00% | 46.67% | 40.00% |
| minicpm-v | LNG_DATASET_SAMPLES_80 | head | 27.63% | 32.81% | 63.64% | 43.30% |
| minicpm-v | LNG_DATASET_SAMPLES_80 | helmet | 25.05% | 26.03% | 86.93% | 40.06% |
| minicpm-v | LNG_DATASET_SAMPLES_80 | person | 29.25% | 29.49% | 97.35% | 45.26% |
| minicpm-v | LNG_DATASET_SAMPLES_80 | alert | 36.07% | 44.00% | 66.67% | 53.01% |

## Analysis and Conclusions

### Cropped Image Recognition (Crop) Experiment

1. **Model Comparison**:
   - gemma3:27b performs best in most scenarios, especially in helmet detection precision
   - minicpm-v performs well with English prompts, in some cases even outperforming gemma3 models
   - gemma3:12b performs consistently with Chinese prompts but is unstable with English prompts

2. **Prompt Language**:
   - All models generally perform better with Chinese prompts than English prompts
   - minicpm-v achieves 100% precision in helmet detection with English prompts

3. **Dataset Characteristics**:
   - Recognition performance on the helmet_sample dataset is generally better than on the lng_output dataset
   - The precision of head_helmet category recognition is generally higher than person category

### Full Image Counting (Count) Experiment

1. **Model Performance**:
   - gemma3:27b performs best in person counting
   - minicpm-v excels in helmet detection, especially on the HELMET_SAMPLES_80 dataset
   - gemma3:12b shows good precision but lower recall rates

2. **Prompt Effectiveness**:
   - detect-prompts configuration works better for the gemma3:27b model
   - count-prompts configuration performs better on the minicpm-v model

3. **Detection Category Difficulty**:
   - person (total count) counting generally has higher accuracy
   - head (without helmet) detection is challenging for all models
   - alert (risk notification) has lower accuracy but generally higher recall rates

## Usage Instructions

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Tests

```bash
# Run all tests
python main.py

# Specify model, prompt file, and dataset
python main.py --model "model_name" --prompt_file "prompt_file" --dataset "dataset_path" --category "category"
```

### Supported Models

- Ollama API models: minicpm-v, gemma3:27b, gemma3:12b, etc.
- GGUF models: Local GGUF files loaded via llama.cpp
- Transformer models: HuggingFace models or local Transformer models 