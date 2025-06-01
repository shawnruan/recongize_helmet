def calculate_metrics(predictions, ground_truths, experiment_type="crop"):
    """计算指标"""
    if experiment_type == "crop":
        return calculate_crop_metrics(predictions, ground_truths)
    elif experiment_type == "binary":
        return calculate_binary_metrics(predictions, ground_truths)
    else:
        return calculate_count_metrics(predictions, ground_truths)

def calculate_crop_metrics(predictions, ground_truths):
    """计算裁剪图片实验的指标"""
    tp = fp = fn = tn = 0
    
    for pred, truth in zip(predictions, ground_truths):
        pred_value = pred.get('helmet', 0)
        true_value = truth.get('class', 0)
        
        if pred_value == 1 and true_value == 1:
            tp += 1
        elif pred_value == 1 and true_value == 0:
            fp += 1
        elif pred_value == 0 and true_value == 1:
            fn += 1
        else:  # pred_value == 0 and true_value == 0
            tn += 1
    
    # 计算总体指标
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0
    
    # 计算Helmet类别（正类）的指标
    helmet_precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    helmet_recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    helmet_f1 = 2 * (helmet_precision * helmet_recall) / (helmet_precision + helmet_recall) if (helmet_precision + helmet_recall) > 0 else 0
    
    # 计算Head类别（负类）的指标
    head_precision = tn / (tn + fn) if (tn + fn) > 0 else 0
    head_recall = tn / (tn + fp) if (tn + fp) > 0 else 0
    head_f1 = 2 * (head_precision * head_recall) / (head_precision + head_recall) if (head_precision + head_recall) > 0 else 0
    
    # 计算F1_macro（两个类别F1的平均值）
    f1_macro = (helmet_f1 + head_f1) / 2
    
    return {
        "accuracy": accuracy,
        "precision": helmet_precision,  # 保持原有的precision（helmet类别）
        "recall": helmet_recall,        # 保持原有的recall（helmet类别）
        "f1_score": helmet_f1,         # 保持原有的f1_score（helmet类别）
        "helmet_precision": helmet_precision,
        "helmet_recall": helmet_recall,
        "helmet_f1": helmet_f1,
        "head_precision": head_precision,
        "head_recall": head_recall,
        "head_f1": head_f1,
        "f1_macro": f1_macro,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn
    }

def calculate_count_metrics(predictions, ground_truths):
    """计算数量统计实验的指标"""
    metrics = {}
    
    for class_name in ["head", "helmet", "person", "alert"]:
        if class_name == "alert":
            # alert的二分类指标计算
            tp = fp = fn = tn = 0
            for pred, truth in zip(predictions, ground_truths):
                pred_value = pred.get(class_name, False)
                true_value = truth[class_name]
                
                if pred_value and true_value:      # True Positive
                    tp += 1
                elif pred_value and not true_value: # False Positive
                    fp += 1
                elif not pred_value and true_value: # False Negative
                    fn += 1
                else:                              # True Negative
                    tn += 1
        else:
            # 对于数值类别(head, helmet, person)，基于总数计算指标
            tp = fp = fn = 0
            tn = 0  # 数值统计中不存在true negative
            
            for pred, truth in zip(predictions, ground_truths):
                pred_count = pred.get(class_name, 0)
                true_count = truth[class_name]
                
                # 计算当前图片中的正确检测、误报和漏检数量
                correct_detections = min(pred_count, true_count)  # 正确检测的数量
                false_positives = max(0, pred_count - true_count) # 误报的数量
                false_negatives = max(0, true_count - pred_count) # 漏检的数量
                
                tp += correct_detections
                fp += false_positives
                fn += false_negatives
        
        # 计算指标
        accuracy = tp / (tp + fp + fn) if (tp + fp + fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics[class_name] = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "true_negatives": tn
        }
    
    return metrics

def calculate_binary_metrics(predictions, ground_truths):
    """计算二分类实验的指标"""
    from config import BINARY_THRESHOLD
    
    tp = fp = fn = tn = 0
    
    for pred, truth in zip(predictions, ground_truths):
        # 获取预测概率值，并根据阈值转换为二分类结果
        pred_probability = pred.get('helmet_probability', 0)
        pred_value = 1 if pred_probability >= BINARY_THRESHOLD else 0
        true_value = truth.get('class', 0)
        
        if pred_value == 1 and true_value == 1:
            tp += 1
        elif pred_value == 1 and true_value == 0:
            fp += 1
        elif pred_value == 0 and true_value == 1:
            fn += 1
        else:  # pred_value == 0 and true_value == 0
            tn += 1
    
    # 计算指标
    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1_score": f1_score,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "threshold": BINARY_THRESHOLD
    } 