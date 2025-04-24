#!/usr/bin/env python3
import json
import os
from datetime import datetime

def format_percentage(value):
    """Convert a float to percentage string with 2 decimal places"""
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"

def extract_base_name(path):
    """Extract the base name from a dataset path"""
    basename = os.path.basename(path)
    if "_output_crops" in basename:
        return basename.replace("_output_crops", "")
    return basename

def main():
    # File paths
    json_path = "/Users/ruanxiaoyang/Desktop/repo/recongize_helmet/result/validation_summary_report.json"
    output_path = "/Users/ruanxiaoyang/Desktop/repo/recongize_helmet/FULL_VALIDATION_REPORT.md"
    
    # Load the JSON data
    with open(json_path, "r") as f:
        data = json.load(f)
    
    # Get all unique models from the data
    all_models = set()
    for report in data["reports"]:
        all_models.add(report["model"])
    
    # Convert to sorted list for consistent ordering
    all_models = sorted(list(all_models))
    print(f"Found {len(all_models)} models: {', '.join(all_models)}")
    
    # Group reports by prompt file and experiment type
    grouped_data = {}
    
    for report in data["reports"]:
        # Extract common data
        model = report["model"]
        dataset_path = report["dataset"]
        dataset = extract_base_name(dataset_path)
        prompt_file_path = report["prompt_file"]
        prompt_file = os.path.basename(prompt_file_path).replace(".md", "")
        experiment_type = report["experiment_type"]
        
        # Create key for grouping
        key = f"{prompt_file}_{experiment_type}"
        if key not in grouped_data:
            grouped_data[key] = []
        
        # Different processing based on experiment type
        if experiment_type == "crop":
            # For crop experiments, metrics are directly in the report
            category = report["category"]
            metrics = report.get("metrics", {})
            timing = report.get("timing", {})
            
            # Extract additional metrics
            tp = metrics.get("true_positives", "N/A")
            fp = metrics.get("false_positives", "N/A")
            tn = metrics.get("true_negatives", "N/A")
            fn = metrics.get("false_negatives", "N/A")
            avg_time = timing.get("average_inference_time", "N/A")
            total_samples = report.get("total_samples", "N/A")
            
            grouped_data[key].append({
                "model": model,
                "dataset": dataset,
                "category": category,
                "accuracy": format_percentage(metrics.get("accuracy")),
                "precision": format_percentage(metrics.get("precision")),
                "recall": format_percentage(metrics.get("recall")),
                "f1_score": format_percentage(metrics.get("f1_score")),
                "true_positives": tp,
                "false_positives": fp,
                "true_negatives": tn,
                "false_negatives": fn,
                "total_samples": total_samples,
                "avg_inference_time": avg_time
            })
        elif experiment_type == "count":
            # For count experiments, metrics are nested by category
            metrics = report.get("metrics", {})
            timing = report.get("timing", {})
            total_samples = report.get("total_samples", "N/A")
            avg_time = timing.get("average_inference_time", "N/A")
            
            # Skip if no metrics
            if not metrics:
                continue
                
            # For count experiments, we have nested metrics by category
            for category, category_metrics in metrics.items():
                # Skip if not a dictionary 
                if not isinstance(category_metrics, dict):
                    continue
                    
                # Get the full dataset name for count experiments
                if "HELMET_SAMPLES_80" in dataset_path:
                    dataset_display = "HELMET_SAMPLES_80"
                elif "LNG_DATASET_SAMPLES_80" in dataset_path:
                    dataset_display = "LNG_DATASET_SAMPLES_80"
                else:
                    dataset_display = dataset
                
                # Extract additional metrics
                tp = category_metrics.get("true_positives", "N/A")
                fp = category_metrics.get("false_positives", "N/A")
                tn = category_metrics.get("true_negatives", "N/A")
                fn = category_metrics.get("false_negatives", "N/A")
                
                grouped_data[key].append({
                    "model": model,
                    "dataset": dataset_display,
                    "category": category,
                    "accuracy": format_percentage(category_metrics.get("accuracy")),
                    "precision": format_percentage(category_metrics.get("precision")),
                    "recall": format_percentage(category_metrics.get("recall")),
                    "f1_score": format_percentage(category_metrics.get("f1_score")),
                    "true_positives": tp,
                    "false_positives": fp,
                    "true_negatives": tn,
                    "false_negatives": fn,
                    "total_samples": total_samples,
                    "avg_inference_time": avg_time
                })
    
    # Sort data within each group by model, dataset, and category
    for key in grouped_data:
        grouped_data[key].sort(key=lambda x: (x["model"], x["dataset"], x["category"]))
    
    # Generate markdown content
    markdown = f"# Complete Validation Results\n\n"
    markdown += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    markdown += f"Total models analyzed: {len(all_models)}\n\n"
    markdown += f"## Models\n\n"
    markdown += ", ".join(all_models) + "\n\n"
    
    # Timing summary if available
    if "timing_summary" in data:
        ts = data["timing_summary"]
        markdown += "## Timing Summary\n\n"
        markdown += f"- Total inference time: {ts.get('total_inference_time', 'N/A')} seconds\n"
        markdown += f"- Total samples: {ts.get('total_samples', 'N/A')}\n"
        markdown += f"- Average inference time: {ts.get('average_inference_time', 'N/A')} seconds per sample\n\n"
    
    # Chinese Prompts
    if "test-prompts_crop" in grouped_data:
        markdown += "## Chinese Prompts (test-prompts.md)\n\n"
        markdown += "| Model | Dataset | Category | Accuracy | Precision | Recall | F1 Score | TP | FP | TN | FN | Samples | Avg Time(s) |\n"
        markdown += "| ----- | ------- | -------- | -------- | --------- | ------ | -------- | -- | -- | -- | -- | ------- | ----------- |\n"
        
        for entry in grouped_data["test-prompts_crop"]:
            markdown += (f"| {entry['model']} | {entry['dataset']} | {entry['category']} | "
                        f"{entry['accuracy']} | {entry['precision']} | {entry['recall']} | {entry['f1_score']} | "
                        f"{entry['true_positives']} | {entry['false_positives']} | {entry['true_negatives']} | "
                        f"{entry['false_negatives']} | {entry['total_samples']} | {entry['avg_inference_time']} |\n")
    
    # English Prompts
    if "test-prompts-en_crop" in grouped_data:
        markdown += "\n## English Prompts (test-prompts-en.md)\n\n"
        markdown += "| Model | Dataset | Category | Accuracy | Precision | Recall | F1 Score | TP | FP | TN | FN | Samples | Avg Time(s) |\n"
        markdown += "| ----- | ------- | -------- | -------- | --------- | ------ | -------- | -- | -- | -- | -- | ------- | ----------- |\n"
        
        for entry in grouped_data["test-prompts-en_crop"]:
            markdown += (f"| {entry['model']} | {entry['dataset']} | {entry['category']} | "
                        f"{entry['accuracy']} | {entry['precision']} | {entry['recall']} | {entry['f1_score']} | "
                        f"{entry['true_positives']} | {entry['false_positives']} | {entry['true_negatives']} | "
                        f"{entry['false_negatives']} | {entry['total_samples']} | {entry['avg_inference_time']} |\n")
    
    # Count task - count-prompts
    if "count-prompts_count" in grouped_data:
        markdown += "\n## Full Image Counting (Count) Task\n\n"
        markdown += "### count-prompts.md\n\n"
        markdown += "| Model | Dataset | Category | Accuracy | Precision | Recall | F1 Score | TP | FP | TN | FN | Samples | Avg Time(s) |\n"
        markdown += "| ----- | ------- | -------- | -------- | --------- | ------ | -------- | -- | -- | -- | -- | ------- | ----------- |\n"
        
        for entry in grouped_data["count-prompts_count"]:
            markdown += (f"| {entry['model']} | {entry['dataset']} | {entry['category']} | "
                        f"{entry['accuracy']} | {entry['precision']} | {entry['recall']} | {entry['f1_score']} | "
                        f"{entry['true_positives']} | {entry['false_positives']} | {entry['true_negatives']} | "
                        f"{entry['false_negatives']} | {entry['total_samples']} | {entry['avg_inference_time']} |\n")
    
    # Count task - detect-prompts
    if "detect-prompts_count" in grouped_data:
        markdown += "\n### detect-prompts.md\n\n"
        markdown += "| Model | Dataset | Category | Accuracy | Precision | Recall | F1 Score | TP | FP | TN | FN | Samples | Avg Time(s) |\n"
        markdown += "| ----- | ------- | -------- | -------- | --------- | ------ | -------- | -- | -- | -- | -- | ------- | ----------- |\n"
        
        for entry in grouped_data["detect-prompts_count"]:
            markdown += (f"| {entry['model']} | {entry['dataset']} | {entry['category']} | "
                        f"{entry['accuracy']} | {entry['precision']} | {entry['recall']} | {entry['f1_score']} | "
                        f"{entry['true_positives']} | {entry['false_positives']} | {entry['true_negatives']} | "
                        f"{entry['false_negatives']} | {entry['total_samples']} | {entry['avg_inference_time']} |\n")
    
    # Add model performance summary
    markdown += "\n## Model Performance Summary\n\n"
    
    # Add section for model comparison
    markdown += "\n## Model Comparison\n\n"
    markdown += "This section provides a comparison of models across different metrics and tasks.\n\n"
    
    # Write to output file
    with open(output_path, "w") as f:
        f.write(markdown)
    
    print(f"Complete validation report generated successfully and saved to {output_path}")

if __name__ == "__main__":
    main() 