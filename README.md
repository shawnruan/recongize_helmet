# Helmet Detection Evaluation System

This project implements a safety helmet wearing detection and statistics system based on vision large models, supporting evaluation of multiple models, multiple prompt configurations, and multiple experiment types.gi

## Project Features

- Support for multiple vision model evaluations (Ollama API, Transformer, GGUF)
- Two evaluation tasks: cropped image object recognition (crop) and full image counting (count)
- Multiple prompt configurations, supporting both Chinese and English
- Comprehensive evaluation metrics calculation
- Results saved in the `result` directory

## Model Performance Comparison

### Cropped Image Object Recognition (Crop) Task

#### Chinese Prompts (test-prompts.md)

| Model           | Dataset       | Category    | Accuracy | Precision | Recall | F1 Score | TP  | FP | TN | FN  | Samples | Avg Time(s) |
| --------------- | ------------- | ----------- | -------- | --------- | ------ | -------- | --- | -- | -- | --- | ------- | ----------- |
| deepseek-janus  | helmet_sample | head_helmet | 60.16%   | 78.85%    | 65.43% | 71.51%   | 123 | 33 | 25 | 65  | 246     | 3.433       |
| deepseek-janus  | helmet_sample | person      | 49.22%   | 49.70%    | 63.08% | 55.59%   | 82  | 83 | 45 | 48  | 258     | 3.444       |
| deepseek-janus  | lng           | head_helmet | 58.60%   | 83.93%    | 61.44% | 70.94%   | 94  | 18 | 15 | 59  | 186     | 3.349       |
| deepseek-janus  | lng           | person      | 52.91%   | 67.57%    | 58.59% | 62.76%   | 75  | 36 | 25 | 53  | 189     | 3.4         |
| deepseek-r1:32b | helmet_sample | head_helmet | 49.19%   | 76.92%    | 47.87% | 59.02%   | 90  | 27 | 31 | 98  | 246     | 3.246       |
| deepseek-r1:32b | helmet_sample | person      | 50.00%   | 50.38%    | 51.54% | 50.95%   | 67  | 66 | 62 | 63  | 258     | 3.595       |
| deepseek-r1:32b | lng           | head_helmet | 51.08%   | 80.39%    | 53.59% | 64.31%   | 82  | 20 | 13 | 71  | 186     | 3.254       |
| deepseek-r1:32b | lng           | person      | 50.79%   | 69.23%    | 49.22% | 57.53%   | 63  | 28 | 33 | 65  | 189     | 3.233       |
| deepseek-r1:7b  | helmet_sample | head_helmet | 35.37%   | 68.83%    | 28.19% | 40.00%   | 53  | 24 | 34 | 135 | 246     | 2.658       |
| deepseek-r1:7b  | helmet_sample | person      | 48.45%   | 48.45%    | 36.15% | 41.41%   | 47  | 50 | 78 | 83  | 258     | 2.755       |
| deepseek-r1:7b  | lng           | head_helmet | 40.86%   | 81.16%    | 36.60% | 50.45%   | 56  | 13 | 20 | 97  | 186     | 2.653       |
| deepseek-r1:7b  | lng           | person      | 45.50%   | 65.82%    | 40.62% | 50.24%   | 52  | 27 | 34 | 76  | 189     | 2.666       |
| gemma3:12b      | helmet_sample | head_helmet | 92.28%   | 95.68%    | 94.15% | 94.91%   | 177 | 8  | 50 | 11  | 246     | 3.099       |
| gemma3:12b      | helmet_sample | person      | 68.22%   | 61.88%    | 96.15% | 75.30%   | 125 | 77 | 51 | 5   | 258     | 3.456       |
| gemma3:12b      | lng           | head_helmet | 71.51%   | 88.46%    | 75.16% | 81.27%   | 115 | 15 | 18 | 38  | 186     | 3.098       |
| gemma3:12b      | lng           | person      | 77.78%   | 78.67%    | 92.19% | 84.89%   | 118 | 32 | 29 | 10  | 189     | 3.107       |
| gemma3:27b      | helmet_sample | head_helmet | 92.28%   | 97.21%    | 92.55% | 94.82%   | 174 | 5  | 53 | 14  | 246     | 3.386       |
| gemma3:27b      | helmet_sample | person      | 70.16%   | 63.32%    | 96.92% | 76.60%   | 126 | 73 | 55 | 4   | 258     | 4.079       |
| gemma3:27b      | lng           | head_helmet | 62.37%   | 87.39%    | 63.40% | 73.48%   | 97  | 14 | 19 | 56  | 186     | 3.39        |
| gemma3:27b      | lng           | person      | 75.13%   | 79.14%    | 85.94% | 82.40%   | 110 | 29 | 32 | 18  | 189     | 3.387       |
| minicpm-o       | helmet_sample | head_helmet | 92.68%   | 96.70%    | 93.62% | 95.14%   | 176 | 6  | 52 | 12  | 246     | 2.745       |
| minicpm-o       | helmet_sample | person      | 70.16%   | 63.32%    | 96.92% | 76.60%   | 126 | 73 | 55 | 4   | 258     | 3.118       |
| minicpm-o       | lng           | head_helmet | 68.82%   | 89.92%    | 69.93% | 78.68%   | 107 | 12 | 21 | 46  | 186     | 2.743       |
| minicpm-o       | lng           | person      | 75.13%   | 79.56%    | 85.16% | 82.26%   | 109 | 28 | 33 | 19  | 189     | 2.738       |
| minicpm-v       | helmet_sample | head_helmet | 91.06%   | 97.70%    | 90.43% | 93.92%   | 170 | 4  | 54 | 18  | 246     | 2.662       |
| minicpm-v       | helmet_sample | person      | 71.71%   | 64.92%    | 95.38% | 77.26%   | 124 | 67 | 61 | 6   | 258     | 2.884       |
| minicpm-v       | lng           | head_helmet | 65.59%   | 92.38%    | 63.40% | 75.19%   | 97  | 8  | 25 | 56  | 186     | 2.661       |
| minicpm-v       | lng           | person      | 74.07%   | 80.15%    | 82.03% | 81.08%   | 105 | 26 | 35 | 23  | 189     | 2.661       |
| qwen2.5-vl-32b  | helmet_sample | head_helmet | 45.53%   | 79.35%    | 38.83% | 52.14%   | 73  | 19 | 39 | 115 | 246     | 3.402       |
| qwen2.5-vl-32b  | helmet_sample | person      | 47.29%   | 47.06%    | 36.92% | 41.38%   | 48  | 54 | 74 | 82  | 258     | 3.966       |
| qwen2.5-vl-32b  | lng           | head_helmet | 44.09%   | 82.67%    | 40.52% | 54.39%   | 62  | 13 | 20 | 91  | 186     | 3.401       |
| qwen2.5-vl-32b  | lng           | person      | 46.56%   | 66.27%    | 42.97% | 52.13%   | 55  | 28 | 33 | 73  | 189     | 3.403       |

#### English Prompts (test-prompts-en.md)

| Model           | Dataset       | Category    | Accuracy | Precision | Recall | F1 Score | TP  | FP | TN | FN  | Samples | Avg Time(s) |
| --------------- | ------------- | ----------- | -------- | --------- | ------ | -------- | --- | -- | -- | --- | ------- | ----------- |
| deepseek-janus  | helmet_sample | head_helmet | 56.50%   | 76.47%    | 62.23% | 68.62%   | 117 | 36 | 22 | 71  | 246     | 3.291       |
| deepseek-janus  | helmet_sample | person      | 48.84%   | 49.29%    | 53.08% | 51.11%   | 69  | 71 | 57 | 61  | 258     | 3.29        |
| deepseek-janus  | lng           | head_helmet | 46.77%   | 77.55%    | 49.67% | 60.56%   | 76  | 22 | 11 | 77  | 186     | 3.28        |
| deepseek-janus  | lng           | person      | 48.68%   | 65.05%    | 52.34% | 58.01%   | 67  | 36 | 25 | 61  | 189     | 3.296       |
| deepseek-r1:32b | helmet_sample | head_helmet | 38.62%   | 76.06%    | 28.72% | 41.70%   | 54  | 17 | 41 | 134 | 246     | 3.576       |
| deepseek-r1:32b | helmet_sample | person      | 51.94%   | 54.17%    | 30.00% | 38.61%   | 39  | 33 | 95 | 91  | 258     | 3.559       |
| deepseek-r1:32b | lng           | head_helmet | 39.78%   | 85.96%    | 32.03% | 46.67%   | 49  | 8  | 25 | 104 | 186     | 3.561       |
| deepseek-r1:32b | lng           | person      | 42.33%   | 71.11%    | 25.00% | 36.99%   | 32  | 13 | 48 | 96  | 189     | 3.57        |
| deepseek-r1:7b  | helmet_sample | head_helmet | 54.47%   | 76.76%    | 57.98% | 66.06%   | 109 | 33 | 25 | 79  | 246     | 2.572       |
| deepseek-r1:7b  | helmet_sample | person      | 51.55%   | 51.77%    | 56.15% | 53.87%   | 73  | 68 | 60 | 57  | 258     | 2.587       |
| deepseek-r1:7b  | lng           | head_helmet | 55.91%   | 82.57%    | 58.82% | 68.70%   | 90  | 19 | 14 | 63  | 186     | 2.589       |
| deepseek-r1:7b  | lng           | person      | 48.68%   | 64.22%    | 54.69% | 59.07%   | 70  | 39 | 22 | 58  | 189     | 2.574       |
| gemma3:12b      | helmet_sample | head_helmet | 70.33%   | 89.66%    | 69.15% | 78.08%   | 130 | 15 | 43 | 58  | 246     | 3.158       |
| gemma3:12b      | helmet_sample | person      | 44.19%   | 39.71%    | 20.77% | 27.27%   | 27  | 41 | 87 | 103 | 258     | 3.172       |
| gemma3:12b      | lng           | head_helmet | 55.91%   | 84.47%    | 56.86% | 67.97%   | 87  | 16 | 17 | 66  | 186     | 3.157       |
| gemma3:12b      | lng           | person      | 66.14%   | 75.81%    | 73.44% | 74.60%   | 94  | 30 | 31 | 34  | 189     | 3.162       |
| gemma3:27b      | helmet_sample | head_helmet | 87.40%   | 99.37%    | 84.04% | 91.07%   | 158 | 1  | 57 | 30  | 246     | 3.42        |
| gemma3:27b      | helmet_sample | person      | 69.77%   | 64.44%    | 89.23% | 74.84%   | 116 | 64 | 64 | 14  | 258     | 3.442       |
| gemma3:27b      | lng           | head_helmet | 56.45%   | 98.65%    | 47.71% | 64.32%   | 73  | 1  | 32 | 80  | 186     | 3.418       |
| gemma3:27b      | lng           | person      | 67.72%   | 80.73%    | 68.75% | 74.26%   | 88  | 21 | 40 | 40  | 189     | 3.429       |
| minicpm-o       | helmet_sample | head_helmet | 93.09%   | 94.76%    | 96.28% | 95.51%   | 181 | 10 | 48 | 7   | 246     | 2.794       |
| minicpm-o       | helmet_sample | person      | 69.77%   | 63.00%    | 96.92% | 76.36%   | 126 | 74 | 54 | 4   | 258     | 2.892       |
| minicpm-o       | lng           | head_helmet | 73.66%   | 87.68%    | 79.08% | 83.16%   | 121 | 17 | 16 | 32  | 186     | 2.792       |
| minicpm-o       | lng           | person      | 76.72%   | 79.58%    | 88.28% | 83.70%   | 113 | 29 | 32 | 15  | 189     | 2.784       |
| minicpm-v       | helmet_sample | head_helmet | 87.40%   | 100.00%   | 83.51% | 91.01%   | 157 | 0  | 58 | 31  | 246     | 2.697       |
| minicpm-v       | helmet_sample | person      | 71.32%   | 65.05%    | 93.08% | 76.58%   | 121 | 65 | 63 | 9   | 258     | 2.787       |
| minicpm-v       | lng           | head_helmet | 40.86%   | 100.00%   | 28.10% | 43.88%   | 43  | 0  | 33 | 110 | 186     | 2.687       |
| minicpm-v       | lng           | person      | 65.61%   | 81.19%    | 64.06% | 71.62%   | 82  | 19 | 42 | 46  | 189     | 2.679       |
| qwen2.5-vl-32b  | helmet_sample | head_helmet | 37.80%   | 75.36%    | 27.66% | 40.47%   | 52  | 17 | 41 | 136 | 246     | 5.087       |
| qwen2.5-vl-32b  | helmet_sample | person      | 52.33%   | 54.55%    | 32.31% | 40.58%   | 42  | 35 | 93 | 88  | 258     | 4.908       |
| qwen2.5-vl-32b  | lng           | head_helmet | 33.33%   | 79.59%    | 25.49% | 38.61%   | 39  | 10 | 23 | 114 | 186     | 4.843       |
| qwen2.5-vl-32b  | lng           | person      | 36.51%   | 58.33%    | 21.88% | 31.82%   | 28  | 20 | 41 | 100 | 189     | 4.985       |

## Full Image Counting (Count) Task

### count-prompts.md

| Model           | Dataset                | Category | Accuracy | Precision | Recall | F1 Score | TP  | FP  | TN | FN  | Samples | Avg Time(s) |
| --------------- | ---------------------- | -------- | -------- | --------- | ------ | -------- | --- | --- | -- | --- | ------- | ----------- |
| deepseek-janus  | HELMET_SAMPLES_80      | alert    | 24.56%   | 34.15%    | 46.67% | 39.44%   | 14  | 27  | 23 | 16  | 80      | 2.928       |
| deepseek-janus  | HELMET_SAMPLES_80      | head     | 11.92%   | 12.39%    | 75.86% | 21.31%   | 44  | 311 | 0  | 14  | 80      | 2.928       |
| deepseek-janus  | HELMET_SAMPLES_80      | helmet   | 30.11%   | 39.26%    | 56.38% | 46.29%   | 106 | 164 | 0  | 82  | 80      | 2.928       |
| deepseek-janus  | HELMET_SAMPLES_80      | person   | 38.28%   | 42.05%    | 81.01% | 55.36%   | 209 | 288 | 0  | 49  | 80      | 2.928       |
| deepseek-janus  | LNG_DATASET_SAMPLES_80 | alert    | 38.18%   | 48.84%    | 63.64% | 55.26%   | 21  | 22  | 25 | 12  | 80      | 2.746       |
| deepseek-janus  | LNG_DATASET_SAMPLES_80 | head     | 6.23%    | 6.43%     | 66.67% | 11.73%   | 22  | 320 | 0  | 11  | 80      | 2.746       |
| deepseek-janus  | LNG_DATASET_SAMPLES_80 | helmet   | 27.54%   | 33.10%    | 62.09% | 43.18%   | 95  | 192 | 0  | 58  | 80      | 2.746       |
| deepseek-janus  | LNG_DATASET_SAMPLES_80 | person   | 32.14%   | 33.96%    | 85.71% | 48.65%   | 162 | 315 | 0  | 27  | 80      | 2.746       |
| deepseek-r1:32b | HELMET_SAMPLES_80      | alert    | 27.42%   | 34.69%    | 56.67% | 43.04%   | 17  | 32  | 18 | 13  | 80      | 4.802       |
| deepseek-r1:32b | HELMET_SAMPLES_80      | head     | 16.31%   | 21.70%    | 39.66% | 28.05%   | 23  | 83  | 0  | 35  | 80      | 4.802       |
| deepseek-r1:32b | HELMET_SAMPLES_80      | helmet   | 39.51%   | 82.65%    | 43.09% | 56.64%   | 81  | 17  | 0  | 107 | 80      | 4.802       |
| deepseek-r1:32b | HELMET_SAMPLES_80      | person   | 46.96%   | 72.77%    | 56.98% | 63.91%   | 147 | 55  | 0  | 111 | 80      | 4.802       |
| deepseek-r1:32b | LNG_DATASET_SAMPLES_80 | alert    | 33.33%   | 41.18%    | 63.64% | 50.00%   | 21  | 30  | 17 | 12  | 80      | 3.928       |
| deepseek-r1:32b | LNG_DATASET_SAMPLES_80 | head     | 16.54%   | 18.26%    | 63.64% | 28.38%   | 21  | 94  | 0  | 12  | 80      | 3.928       |
| deepseek-r1:32b | LNG_DATASET_SAMPLES_80 | helmet   | 36.81%   | 69.79%    | 43.79% | 53.82%   | 67  | 29  | 0  | 86  | 80      | 3.928       |
| deepseek-r1:32b | LNG_DATASET_SAMPLES_80 | person   | 44.24%   | 58.02%    | 65.08% | 61.35%   | 123 | 89  | 0  | 66  | 80      | 3.928       |
| deepseek-r1:7b  | HELMET_SAMPLES_80      | alert    | 9.76%    | 26.67%    | 13.33% | 17.78%   | 4   | 11  | 39 | 26  | 80      | 3.181       |
| deepseek-r1:7b  | HELMET_SAMPLES_80      | head     | 18.33%   | 26.19%    | 37.93% | 30.99%   | 22  | 62  | 0  | 36  | 80      | 3.181       |
| deepseek-r1:7b  | HELMET_SAMPLES_80      | helmet   | 35.84%   | 52.36%    | 53.19% | 52.77%   | 100 | 91  | 0  | 88  | 80      | 3.181       |
| deepseek-r1:7b  | HELMET_SAMPLES_80      | person   | 38.73%   | 55.09%    | 56.59% | 55.83%   | 146 | 119 | 0  | 112 | 80      | 3.181       |
| deepseek-r1:7b  | LNG_DATASET_SAMPLES_80 | alert    | 7.50%    | 30.00%    | 9.09%  | 13.95%   | 3   | 7   | 40 | 30  | 80      | 2.96        |
| deepseek-r1:7b  | LNG_DATASET_SAMPLES_80 | head     | 11.72%   | 13.64%    | 45.45% | 20.98%   | 15  | 95  | 0  | 18  | 80      | 2.96        |
| deepseek-r1:7b  | LNG_DATASET_SAMPLES_80 | helmet   | 34.09%   | 40.38%    | 68.63% | 50.85%   | 105 | 155 | 0  | 48  | 80      | 2.96        |
| deepseek-r1:7b  | LNG_DATASET_SAMPLES_80 | person   | 36.96%   | 41.48%    | 77.25% | 53.97%   | 146 | 206 | 0  | 43  | 80      | 2.96        |
| gemma3:12b      | HELMET_SAMPLES_80      | alert    | 42.19%   | 44.26%    | 90.00% | 59.34%   | 27  | 34  | 16 | 3   | 80      | 3.959       |
| gemma3:12b      | HELMET_SAMPLES_80      | head     | 35.65%   | 41.84%    | 70.69% | 52.56%   | 41  | 57  | 0  | 17  | 80      | 3.959       |
| gemma3:12b      | HELMET_SAMPLES_80      | helmet   | 44.44%   | 89.80%    | 46.81% | 61.54%   | 88  | 10  | 0  | 100 | 80      | 3.959       |
| gemma3:12b      | HELMET_SAMPLES_80      | person   | 70.04%   | 95.41%    | 72.48% | 82.38%   | 187 | 9   | 0  | 71  | 80      | 3.959       |
| gemma3:12b      | LNG_DATASET_SAMPLES_80 | alert    | 34.04%   | 53.33%    | 48.48% | 50.79%   | 16  | 14  | 33 | 17  | 80      | 3.746       |
| gemma3:12b      | LNG_DATASET_SAMPLES_80 | head     | 30.19%   | 44.44%    | 48.48% | 46.38%   | 16  | 20  | 0  | 17  | 80      | 3.746       |
| gemma3:12b      | LNG_DATASET_SAMPLES_80 | helmet   | 43.20%   | 62.68%    | 58.17% | 60.34%   | 89  | 53  | 0  | 64  | 80      | 3.746       |
| gemma3:12b      | LNG_DATASET_SAMPLES_80 | person   | 52.92%   | 71.35%    | 67.20% | 69.21%   | 127 | 51  | 0  | 62  | 80      | 3.746       |
| gemma3:27b      | HELMET_SAMPLES_80      | alert    | 48.33%   | 49.15%    | 96.67% | 65.17%   | 29  | 30  | 20 | 1   | 80      | 6.514       |
| gemma3:27b      | HELMET_SAMPLES_80      | head     | 48.15%   | 50.98%    | 89.66% | 65.00%   | 52  | 50  | 0  | 6   | 80      | 6.514       |
| gemma3:27b      | HELMET_SAMPLES_80      | helmet   | 70.41%   | 94.52%    | 73.40% | 82.63%   | 138 | 8   | 0  | 50  | 80      | 6.514       |
| gemma3:27b      | HELMET_SAMPLES_80      | person   | 85.35%   | 93.95%    | 90.31% | 92.09%   | 233 | 15  | 0  | 25  | 80      | 6.514       |
| gemma3:27b      | LNG_DATASET_SAMPLES_80 | alert    | 31.58%   | 42.86%    | 54.55% | 48.00%   | 18  | 24  | 23 | 15  | 80      | 4.417       |
| gemma3:27b      | LNG_DATASET_SAMPLES_80 | head     | 27.69%   | 36.00%    | 54.55% | 43.37%   | 18  | 32  | 0  | 15  | 80      | 4.417       |
| gemma3:27b      | LNG_DATASET_SAMPLES_80 | helmet   | 43.98%   | 68.85%    | 54.90% | 61.09%   | 84  | 38  | 0  | 69  | 80      | 4.417       |
| gemma3:27b      | LNG_DATASET_SAMPLES_80 | person   | 57.21%   | 76.61%    | 69.31% | 72.78%   | 131 | 40  | 0  | 58  | 80      | 4.417       |
| minicpm-o       | HELMET_SAMPLES_80      | alert    | 64.44%   | 65.91%    | 96.67% | 78.38%   | 29  | 15  | 35 | 1   | 80      | 4.668       |
| minicpm-o       | HELMET_SAMPLES_80      | head     | 55.95%   | 64.38%    | 81.03% | 71.76%   | 47  | 26  | 0  | 11  | 80      | 4.668       |
| minicpm-o       | HELMET_SAMPLES_80      | helmet   | 78.79%   | 93.98%    | 82.98% | 88.14%   | 156 | 10  | 0  | 32  | 80      | 4.668       |
| minicpm-o       | HELMET_SAMPLES_80      | person   | 86.30%   | 95.10%    | 90.31% | 92.64%   | 233 | 12  | 0  | 25  | 80      | 4.668       |
| minicpm-o       | LNG_DATASET_SAMPLES_80 | alert    | 25.00%   | 40.62%    | 39.39% | 40.00%   | 13  | 19  | 28 | 20  | 80      | 4.973       |
| minicpm-o       | LNG_DATASET_SAMPLES_80 | head     | 20.37%   | 34.38%    | 33.33% | 33.85%   | 11  | 21  | 0  | 22  | 80      | 4.973       |
| minicpm-o       | LNG_DATASET_SAMPLES_80 | helmet   | 63.54%   | 80.42%    | 75.16% | 77.70%   | 115 | 28  | 0  | 38  | 80      | 4.973       |
| minicpm-o       | LNG_DATASET_SAMPLES_80 | person   | 75.34%   | 84.62%    | 87.30% | 85.94%   | 165 | 30  | 0  | 24  | 80      | 4.973       |
| minicpm-v       | HELMET_SAMPLES_80      | alert    | 54.72%   | 55.77%    | 96.67% | 70.73%   | 29  | 23  | 27 | 1   | 80      | 3.651       |
| minicpm-v       | HELMET_SAMPLES_80      | head     | 44.54%   | 46.49%    | 91.38% | 61.63%   | 53  | 61  | 0  | 5   | 80      | 3.651       |
| minicpm-v       | HELMET_SAMPLES_80      | helmet   | 76.73%   | 91.72%    | 82.45% | 86.83%   | 155 | 14  | 0  | 33  | 80      | 3.651       |
| minicpm-v       | HELMET_SAMPLES_80      | person   | 80.73%   | 84.97%    | 94.19% | 89.34%   | 243 | 43  | 0  | 15  | 80      | 3.651       |
| minicpm-v       | LNG_DATASET_SAMPLES_80 | alert    | 30.16%   | 38.78%    | 57.58% | 46.34%   | 19  | 30  | 17 | 14  | 80      | 4.45        |
| minicpm-v       | LNG_DATASET_SAMPLES_80 | head     | 12.00%   | 15.19%    | 36.36% | 21.43%   | 12  | 67  | 0  | 21  | 80      | 4.45        |
| minicpm-v       | LNG_DATASET_SAMPLES_80 | helmet   | 64.29%   | 87.80%    | 70.59% | 78.26%   | 108 | 15  | 0  | 45  | 80      | 4.45        |
| minicpm-v       | LNG_DATASET_SAMPLES_80 | person   | 66.80%   | 71.19%    | 91.53% | 80.09%   | 173 | 70  | 0  | 16  | 80      | 4.45        |
| qwen2.5-vl-32b  | HELMET_SAMPLES_80      | alert    | 30.51%   | 38.30%    | 60.00% | 46.75%   | 18  | 29  | 21 | 12  | 80      | 6.598       |
| qwen2.5-vl-32b  | HELMET_SAMPLES_80      | head     | 16.28%   | 22.83%    | 36.21% | 28.00%   | 21  | 71  | 0  | 37  | 80      | 6.598       |
| qwen2.5-vl-32b  | HELMET_SAMPLES_80      | helmet   | 28.16%   | 76.32%    | 30.85% | 43.94%   | 58  | 18  | 0  | 130 | 80      | 6.598       |
| qwen2.5-vl-32b  | HELMET_SAMPLES_80      | person   | 42.00%   | 75.00%    | 48.84% | 59.15%   | 126 | 42  | 0  | 132 | 80      | 6.598       |
| qwen2.5-vl-32b  | LNG_DATASET_SAMPLES_80 | alert    | 26.42%   | 41.18%    | 42.42% | 41.79%   | 14  | 20  | 27 | 19  | 80      | 4.868       |
| qwen2.5-vl-32b  | LNG_DATASET_SAMPLES_80 | head     | 13.86%   | 17.07%    | 42.42% | 24.35%   | 14  | 68  | 0  | 19  | 80      | 4.868       |
| qwen2.5-vl-32b  | LNG_DATASET_SAMPLES_80 | helmet   | 30.41%   | 59.00%    | 38.56% | 46.64%   | 59  | 41  | 0  | 94  | 80      | 4.868       |
| qwen2.5-vl-32b  | LNG_DATASET_SAMPLES_80 | person   | 43.58%   | 62.22%    | 59.26% | 60.70%   | 112 | 68  | 0  | 77  | 80      | 4.868       |

### detect-prompts.md

| Model           | Dataset                | Category | Accuracy | Precision | Recall  | F1 Score | TP  | FP  | TN | FN  | Samples | Avg Time(s) |
| --------------- | ---------------------- | -------- | -------- | --------- | ------- | -------- | --- | --- | -- | --- | ------- | ----------- |
| deepseek-janus  | HELMET_SAMPLES_80      | alert    | 28.85%   | 40.54%    | 50.00%  | 44.78%   | 15  | 22  | 28 | 15  | 80      | 2.579       |
| deepseek-janus  | HELMET_SAMPLES_80      | head     | 13.16%   | 14.40%    | 60.34%  | 23.26%   | 35  | 208 | 0  | 23  | 80      | 2.579       |
| deepseek-janus  | HELMET_SAMPLES_80      | helmet   | 33.10%   | 37.08%    | 75.53%  | 49.74%   | 142 | 241 | 0  | 46  | 80      | 2.579       |
| deepseek-janus  | HELMET_SAMPLES_80      | person   | 40.73%   | 43.41%    | 86.82%  | 57.88%   | 224 | 292 | 0  | 34  | 80      | 2.579       |
| deepseek-janus  | LNG_DATASET_SAMPLES_80 | alert    | 25.00%   | 37.84%    | 42.42%  | 40.00%   | 14  | 23  | 24 | 19  | 80      | 2.623       |
| deepseek-janus  | LNG_DATASET_SAMPLES_80 | head     | 12.30%   | 12.45%    | 90.91%  | 21.90%   | 30  | 211 | 0  | 3   | 80      | 2.623       |
| deepseek-janus  | LNG_DATASET_SAMPLES_80 | helmet   | 26.51%   | 30.70%    | 66.01%  | 41.91%   | 101 | 228 | 0  | 52  | 80      | 2.623       |
| deepseek-janus  | LNG_DATASET_SAMPLES_80 | person   | 33.47%   | 35.01%    | 88.36%  | 50.15%   | 167 | 310 | 0  | 22  | 80      | 2.623       |
| deepseek-r1:32b | HELMET_SAMPLES_80      | alert    | 15.69%   | 27.59%    | 26.67%  | 27.12%   | 8   | 21  | 29 | 22  | 80      | 3.903       |
| deepseek-r1:32b | HELMET_SAMPLES_80      | head     | 10.87%   | 22.73%    | 17.24%  | 19.61%   | 10  | 34  | 0  | 48  | 80      | 3.903       |
| deepseek-r1:32b | HELMET_SAMPLES_80      | helmet   | 47.96%   | 57.09%    | 75.00%  | 64.83%   | 141 | 106 | 0  | 47  | 80      | 3.903       |
| deepseek-r1:32b | HELMET_SAMPLES_80      | person   | 53.35%   | 65.64%    | 74.03%  | 69.58%   | 191 | 100 | 0  | 67  | 80      | 3.903       |
| deepseek-r1:32b | LNG_DATASET_SAMPLES_80 | alert    | 17.31%   | 32.14%    | 27.27%  | 29.51%   | 9   | 19  | 28 | 24  | 80      | 3.925       |
| deepseek-r1:32b | LNG_DATASET_SAMPLES_80 | head     | 13.24%   | 20.45%    | 27.27%  | 23.38%   | 9   | 35  | 0  | 24  | 80      | 3.925       |
| deepseek-r1:32b | LNG_DATASET_SAMPLES_80 | helmet   | 49.81%   | 55.17%    | 83.66%  | 66.49%   | 128 | 104 | 0  | 25  | 80      | 3.925       |
| deepseek-r1:32b | LNG_DATASET_SAMPLES_80 | person   | 52.46%   | 57.97%    | 84.66%  | 68.82%   | 160 | 116 | 0  | 29  | 80      | 3.925       |
| deepseek-r1:7b  | HELMET_SAMPLES_80      | alert    | 32.79%   | 39.22%    | 66.67%  | 49.38%   | 20  | 31  | 19 | 10  | 80      | 2.861       |
| deepseek-r1:7b  | HELMET_SAMPLES_80      | head     | 15.81%   | 17.37%    | 63.79%  | 27.31%   | 37  | 176 | 0  | 21  | 80      | 2.861       |
| deepseek-r1:7b  | HELMET_SAMPLES_80      | helmet   | 45.76%   | 49.39%    | 86.17%  | 62.79%   | 162 | 166 | 0  | 26  | 80      | 2.861       |
| deepseek-r1:7b  | HELMET_SAMPLES_80      | person   | 42.71%   | 43.86%    | 94.19%  | 59.85%   | 243 | 311 | 0  | 15  | 80      | 2.861       |
| deepseek-r1:7b  | LNG_DATASET_SAMPLES_80 | alert    | 38.24%   | 42.62%    | 78.79%  | 55.32%   | 26  | 35  | 12 | 7   | 80      | 2.901       |
| deepseek-r1:7b  | LNG_DATASET_SAMPLES_80 | head     | 10.32%   | 10.61%    | 78.79%  | 18.71%   | 26  | 219 | 0  | 7   | 80      | 2.901       |
| deepseek-r1:7b  | LNG_DATASET_SAMPLES_80 | helmet   | 39.24%   | 41.41%    | 88.24%  | 56.37%   | 135 | 191 | 0  | 18  | 80      | 2.901       |
| deepseek-r1:7b  | LNG_DATASET_SAMPLES_80 | person   | 32.16%   | 32.50%    | 96.83%  | 48.67%   | 183 | 380 | 0  | 6   | 80      | 2.901       |
| gemma3:12b      | HELMET_SAMPLES_80      | alert    | 37.50%   | 37.50%    | 100.00% | 54.55%   | 30  | 50  | 0  | 0   | 80      | 3.573       |
| gemma3:12b      | HELMET_SAMPLES_80      | head     | 32.19%   | 34.81%    | 81.03%  | 48.70%   | 47  | 88  | 0  | 11  | 80      | 3.573       |
| gemma3:12b      | HELMET_SAMPLES_80      | helmet   | 50.00%   | 80.45%    | 56.91%  | 66.67%   | 107 | 26  | 0  | 81  | 80      | 3.573       |
| gemma3:12b      | HELMET_SAMPLES_80      | person   | 69.03%   | 80.45%    | 82.95%  | 81.68%   | 214 | 52  | 0  | 44  | 80      | 3.573       |
| gemma3:12b      | LNG_DATASET_SAMPLES_80 | alert    | 41.03%   | 41.56%    | 96.97%  | 58.18%   | 32  | 45  | 2  | 1   | 80      | 3.678       |
| gemma3:12b      | LNG_DATASET_SAMPLES_80 | head     | 25.20%   | 25.40%    | 96.97%  | 40.25%   | 32  | 94  | 0  | 1   | 80      | 3.678       |
| gemma3:12b      | LNG_DATASET_SAMPLES_80 | helmet   | 37.93%   | 42.16%    | 79.08%  | 55.00%   | 121 | 166 | 0  | 32  | 80      | 3.678       |
| gemma3:12b      | LNG_DATASET_SAMPLES_80 | person   | 37.91%   | 40.35%    | 86.24%  | 54.97%   | 163 | 241 | 0  | 26  | 80      | 3.678       |
| gemma3:27b      | HELMET_SAMPLES_80      | alert    | 54.90%   | 57.14%    | 93.33%  | 70.89%   | 28  | 21  | 29 | 2   | 80      | 4.191       |
| gemma3:27b      | HELMET_SAMPLES_80      | head     | 51.65%   | 58.75%    | 81.03%  | 68.12%   | 47  | 33  | 0  | 11  | 80      | 4.191       |
| gemma3:27b      | HELMET_SAMPLES_80      | helmet   | 74.13%   | 91.98%    | 79.26%  | 85.14%   | 149 | 13  | 0  | 39  | 80      | 4.191       |
| gemma3:27b      | HELMET_SAMPLES_80      | person   | 85.13%   | 95.42%    | 88.76%  | 91.97%   | 229 | 11  | 0  | 29  | 80      | 4.191       |
| gemma3:27b      | LNG_DATASET_SAMPLES_80 | alert    | 44.93%   | 46.27%    | 93.94%  | 62.00%   | 31  | 36  | 11 | 2   | 80      | 4.1         |
| gemma3:27b      | LNG_DATASET_SAMPLES_80 | head     | 35.23%   | 36.05%    | 93.94%  | 52.10%   | 31  | 55  | 0  | 2   | 80      | 4.1         |
| gemma3:27b      | LNG_DATASET_SAMPLES_80 | helmet   | 42.35%   | 65.87%    | 54.25%  | 59.50%   | 83  | 43  | 0  | 70  | 80      | 4.1         |
| gemma3:27b      | LNG_DATASET_SAMPLES_80 | person   | 53.64%   | 66.04%    | 74.07%  | 69.83%   | 140 | 72  | 0  | 49  | 80      | 4.1         |
| minicpm-o       | HELMET_SAMPLES_80      | alert    | 40.62%   | 43.33%    | 86.67%  | 57.78%   | 26  | 34  | 16 | 4   | 80      | 3.703       |
| minicpm-o       | HELMET_SAMPLES_80      | head     | 31.31%   | 43.06%    | 53.45%  | 47.69%   | 31  | 41  | 0  | 27  | 80      | 3.703       |
| minicpm-o       | HELMET_SAMPLES_80      | helmet   | 78.95%   | 88.71%    | 87.77%  | 88.24%   | 165 | 21  | 0  | 23  | 80      | 3.703       |
| minicpm-o       | HELMET_SAMPLES_80      | person   | 83.33%   | 88.89%    | 93.02%  | 90.91%   | 240 | 30  | 0  | 18  | 80      | 3.703       |
| minicpm-o       | LNG_DATASET_SAMPLES_80 | alert    | 42.25%   | 44.12%    | 90.91%  | 59.41%   | 30  | 38  | 9  | 3   | 80      | 4.937       |
| minicpm-o       | LNG_DATASET_SAMPLES_80 | head     | 37.04%   | 38.46%    | 90.91%  | 54.05%   | 30  | 48  | 0  | 3   | 80      | 4.937       |
| minicpm-o       | LNG_DATASET_SAMPLES_80 | helmet   | 66.08%   | 86.26%    | 73.86%  | 79.58%   | 113 | 18  | 0  | 40  | 80      | 4.937       |
| minicpm-o       | LNG_DATASET_SAMPLES_80 | person   | 74.79%   | 77.35%    | 95.77%  | 85.58%   | 181 | 53  | 0  | 8   | 80      | 4.937       |
| minicpm-v       | HELMET_SAMPLES_80      | alert    | 26.00%   | 39.39%    | 43.33%  | 41.27%   | 13  | 20  | 30 | 17  | 80      | 3.29        |
| minicpm-v       | HELMET_SAMPLES_80      | head     | 17.98%   | 34.04%    | 27.59%  | 30.48%   | 16  | 31  | 0  | 42  | 80      | 3.29        |
| minicpm-v       | HELMET_SAMPLES_80      | helmet   | 73.00%   | 77.93%    | 92.02%  | 84.39%   | 173 | 49  | 0  | 15  | 80      | 3.29        |
| minicpm-v       | HELMET_SAMPLES_80      | person   | 79.28%   | 83.97%    | 93.41%  | 88.44%   | 241 | 46  | 0  | 17  | 80      | 3.29        |
| minicpm-v       | LNG_DATASET_SAMPLES_80 | alert    | 33.33%   | 42.55%    | 60.61%  | 50.00%   | 20  | 27  | 20 | 13  | 80      | 4.416       |
| minicpm-v       | LNG_DATASET_SAMPLES_80 | head     | 23.46%   | 28.36%    | 57.58%  | 38.00%   | 19  | 48  | 0  | 14  | 80      | 4.416       |
| minicpm-v       | LNG_DATASET_SAMPLES_80 | helmet   | 39.32%   | 42.76%    | 83.01%  | 56.44%   | 127 | 170 | 0  | 26  | 80      | 4.416       |
| minicpm-v       | LNG_DATASET_SAMPLES_80 | person   | 47.64%   | 48.53%    | 96.30%  | 64.54%   | 182 | 193 | 0  | 7   | 80      | 4.416       |
| qwen2.5-vl-32b  | HELMET_SAMPLES_80      | alert    | 37.04%   | 45.45%    | 66.67%  | 54.05%   | 20  | 24  | 26 | 10  | 80      | 9.051       |
| qwen2.5-vl-32b  | HELMET_SAMPLES_80      | head     | 5.22%    | 6.25%     | 24.14%  | 9.93%    | 14  | 210 | 0  | 44  | 80      | 9.051       |
| qwen2.5-vl-32b  | HELMET_SAMPLES_80      | helmet   | 16.87%   | 28.50%    | 29.26%  | 28.87%   | 55  | 138 | 0  | 133 | 80      | 9.051       |
| qwen2.5-vl-32b  | HELMET_SAMPLES_80      | person   | 20.05%   | 37.93%    | 29.84%  | 33.41%   | 77  | 126 | 0  | 181 | 80      | 9.051       |
| qwen2.5-vl-32b  | LNG_DATASET_SAMPLES_80 | alert    | 26.56%   | 35.42%    | 51.52%  | 41.98%   | 17  | 31  | 16 | 16  | 80      | 9.08        |
| qwen2.5-vl-32b  | LNG_DATASET_SAMPLES_80 | head     | 3.83%    | 4.20%     | 30.30%  | 7.38%    | 10  | 228 | 0  | 23  | 80      | 9.08        |
| qwen2.5-vl-32b  | LNG_DATASET_SAMPLES_80 | helmet   | 15.81%   | 22.81%    | 33.99%  | 27.30%   | 52  | 176 | 0  | 101 | 80      | 9.08        |
| qwen2.5-vl-32b  | LNG_DATASET_SAMPLES_80 | person   | 19.16%   | 27.55%    | 38.62%  | 32.16%   | 73  | 192 | 0  | 116 | 80      | 9.08        |

## Usage Instructions

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Tests

```bash
# Run all tests
python main.py


### Supported Models

- Ollama API models: minicpm-v, gemma3:27b, gemma3:12b
```
