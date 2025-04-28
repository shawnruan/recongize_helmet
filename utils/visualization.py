import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
from config import BINARY_THRESHOLD
from collections import Counter

def ensure_picture_dir():
    """Ensure the picture directory exists"""
    os.makedirs('result/picture', exist_ok=True)

def plot_score_distribution(results, dataset_name, category, model_name, prompt_name, experiment_type):
    """Generate score distribution charts
    
    Args:
        results: List of results, each containing a score field
        dataset_name: Dataset name
        category: Category name
        model_name: Model name
        prompt_name: Prompt configuration name
        experiment_type: Experiment type
    """
    ensure_picture_dir()
    
    # Clean special characters for use in filenames
    safe_dataset = os.path.basename(dataset_name)
    safe_model = model_name.replace(':', '_')
    safe_prompt = os.path.basename(prompt_name).replace('.md', '')
    
    # Extract all scores and labels
    scores = [r.get('score', 0) for r in results]
    ground_truths = [r.get('ground_truth', 0) for r in results]
    
    # Only generate plots for binary classification experiments
    if experiment_type == 'binary' and scores:
        # Set style
        plt.style.use('ggplot')
        
        # Separate positive and negative sample scores
        positive_scores = [scores[i] for i in range(len(scores)) if ground_truths[i] == 1]
        negative_scores = [scores[i] for i in range(len(scores)) if ground_truths[i] == 0]
        positive_indices = [i for i in range(len(scores)) if ground_truths[i] == 1]
        negative_indices = [i for i in range(len(scores)) if ground_truths[i] == 0]
        
        # Extract probability values
        probabilities = [r.get('probability', 0) for r in results]
        positive_probs = [probabilities[i] for i in range(len(probabilities)) if ground_truths[i] == 1]
        negative_probs = [probabilities[i] for i in range(len(probabilities)) if ground_truths[i] == 0]
        
        threshold_score = BINARY_THRESHOLD * 100
        
        # Dictionary to store all generated chart paths
        paths = {}
        
        # 1. Create combined score distribution line chart
        plt.figure(figsize=(12, 7))
        
        # Create histograms and convert to line charts
        bins = np.arange(0, 101, 5)  # Bins from 0 to 100 in steps of 5
        
        # Count samples in each bin
        pos_counts, pos_bins = np.histogram(positive_scores, bins=bins)
        neg_counts, neg_bins = np.histogram(negative_scores, bins=bins)
        
        # Plot lines at bin centers
        bin_centers = (bins[:-1] + bins[1:]) / 2
        plt.plot(bin_centers, pos_counts, 'o-', color='green', linewidth=2, 
                 label='Positive (With Helmet)')
        plt.plot(bin_centers, neg_counts, 'o-', color='red', linewidth=2, 
                 label='Negative (Without Helmet)')
        
        # Mark threshold line
        plt.axvline(x=threshold_score, color='blue', linestyle='--', 
                   label=f'Threshold ({threshold_score})')
        
        # Set chart properties
        plt.title(f'{safe_dataset} - {category} Score Distribution')
        plt.xlabel('Score')
        plt.ylabel('Count')
        plt.legend()
        plt.grid(True)
        
        # Set X axis range from 0-100
        plt.xlim(0, 100)
        
        # Make sure Y axis starts at zero
        plt.ylim(bottom=0)
        
        # Save the image
        curve_path = f'result/picture/{safe_dataset}_{category}_{safe_model}_{safe_prompt}_score_distribution.png'
        plt.savefig(curve_path)
        plt.close()
        
        print(f"Score distribution chart saved to: {curve_path}")
        paths['score_distribution'] = curve_path
        
        # 2. Create separate charts for positive and negative samples
        # 2.1 Positive sample score distribution
        if positive_scores:
            plt.figure(figsize=(12, 7))
            pos_counts, pos_bins = np.histogram(positive_scores, bins=bins)
            plt.plot(bin_centers, pos_counts, 'o-', color='green', linewidth=2)
            plt.axvline(x=threshold_score, color='blue', linestyle='--', 
                       label=f'Threshold ({threshold_score})')
            plt.title(f'{safe_dataset} - {category} Positive Sample Score Distribution')
            plt.xlabel('Score')
            plt.ylabel('Count')
            plt.legend(['Positive (With Helmet)', f'Threshold ({threshold_score})'])
            plt.grid(True)
            plt.xlim(0, 100)
            plt.ylim(bottom=0)
            
            positive_curve_path = f'result/picture/{safe_dataset}_{category}_{safe_model}_{safe_prompt}_positive_score_distribution.png'
            plt.savefig(positive_curve_path)
            plt.close()
            print(f"Positive sample score distribution chart saved to: {positive_curve_path}")
            paths['positive_score_distribution'] = positive_curve_path
        
        # 2.2 Negative sample score distribution
        if negative_scores:
            plt.figure(figsize=(12, 7))
            neg_counts, neg_bins = np.histogram(negative_scores, bins=bins)
            plt.plot(bin_centers, neg_counts, 'o-', color='red', linewidth=2)
            plt.axvline(x=threshold_score, color='blue', linestyle='--', 
                       label=f'Threshold ({threshold_score})')
            plt.title(f'{safe_dataset} - {category} Negative Sample Score Distribution')
            plt.xlabel('Score')
            plt.ylabel('Count')
            plt.legend(['Negative (Without Helmet)', f'Threshold ({threshold_score})'])
            plt.grid(True)
            plt.xlim(0, 100)
            plt.ylim(bottom=0)
            
            negative_curve_path = f'result/picture/{safe_dataset}_{category}_{safe_model}_{safe_prompt}_negative_score_distribution.png'
            plt.savefig(negative_curve_path)
            plt.close()
            print(f"Negative sample score distribution chart saved to: {negative_curve_path}")
            paths['negative_score_distribution'] = negative_curve_path
        
        # 3. Create scatter plot with scores
        plt.figure(figsize=(12, 7))
        
        # Create a jitter effect to see multiple points with the same score
        jitter = 0.3
        
        # Generate slight random jitter for Y axis
        if positive_indices:
            y_pos = np.random.normal(1, jitter, len(positive_indices))
            plt.scatter([scores[i] for i in positive_indices], y_pos, 
                      label='Positive (With Helmet)', color='green', alpha=0.7)
            
        if negative_indices:
            y_neg = np.random.normal(0, jitter, len(negative_indices))
            plt.scatter([scores[i] for i in negative_indices], y_neg, 
                      label='Negative (Without Helmet)', color='red', alpha=0.7)
        
        # Mark threshold line
        plt.axvline(x=threshold_score, color='blue', linestyle='--', 
                   label=f'Threshold ({threshold_score})')
        
        # Set chart properties
        plt.title(f'{safe_dataset} - {category} Score Scatter Plot')
        plt.xlabel('Score')
        plt.yticks([0, 1], ['Without Helmet', 'With Helmet'])
        plt.legend()
        plt.grid(True)
        
        # Set X axis range from 0-100
        plt.xlim(0, 100)
        plt.ylim(-0.5, 1.5)
        
        # Save the image
        scatter_path = f'result/picture/{safe_dataset}_{category}_{safe_model}_{safe_prompt}_score_scatter.png'
        plt.savefig(scatter_path)
        plt.close()
        
        print(f"Score scatter plot saved to: {scatter_path}")
        paths['score_scatter'] = scatter_path
        
        # 4. Create probability distributions as line charts (not KDE)
        plt.figure(figsize=(12, 7))
        
        # Create histogram with probability bins
        prob_bins = np.arange(0, 1.05, 0.05)  # 0 to 1 in steps of 0.05
        
        # Count samples in each probability bin
        pos_prob_counts, pos_prob_bins = np.histogram(positive_probs, bins=prob_bins)
        neg_prob_counts, neg_prob_bins = np.histogram(negative_probs, bins=prob_bins)
        
        # Plot lines at bin centers
        prob_bin_centers = (prob_bins[:-1] + prob_bins[1:]) / 2
        plt.plot(prob_bin_centers, pos_prob_counts, 'o-', color='green', linewidth=2, 
                 label='Positive (With Helmet)')
        plt.plot(prob_bin_centers, neg_prob_counts, 'o-', color='red', linewidth=2, 
                 label='Negative (Without Helmet)')
        
        # Mark threshold line
        plt.axvline(x=BINARY_THRESHOLD, color='blue', linestyle='--', 
                   label=f'Threshold ({BINARY_THRESHOLD})')
        
        # Set chart properties
        plt.title(f'{safe_dataset} - {category} Probability Distribution')
        plt.xlabel('Probability')
        plt.ylabel('Count')
        plt.legend()
        plt.grid(True)
        
        # Set X axis range from 0-1
        plt.xlim(0, 1)
        plt.ylim(bottom=0)
        
        # Save the image
        prob_path = f'result/picture/{safe_dataset}_{category}_{safe_model}_{safe_prompt}_probability_distribution.png'
        plt.savefig(prob_path)
        plt.close()
        
        print(f"Probability distribution chart saved to: {prob_path}")
        paths['probability_distribution'] = prob_path
        
        # 5. Separate probability distribution charts
        # 5.1 Positive sample probability distribution
        if positive_probs:
            plt.figure(figsize=(12, 7))
            pos_prob_counts, _ = np.histogram(positive_probs, bins=prob_bins)
            plt.plot(prob_bin_centers, pos_prob_counts, 'o-', color='green', linewidth=2)
            plt.axvline(x=BINARY_THRESHOLD, color='blue', linestyle='--', 
                       label=f'Threshold ({BINARY_THRESHOLD})')
            plt.title(f'{safe_dataset} - {category} Positive Sample Probability Distribution')
            plt.xlabel('Probability')
            plt.ylabel('Count')
            plt.legend(['Positive (With Helmet)', f'Threshold ({BINARY_THRESHOLD})'])
            plt.grid(True)
            plt.xlim(0, 1)
            plt.ylim(bottom=0)
            
            pos_prob_path = f'result/picture/{safe_dataset}_{category}_{safe_model}_{safe_prompt}_positive_probability_distribution.png'
            plt.savefig(pos_prob_path)
            plt.close()
            print(f"Positive sample probability distribution chart saved to: {pos_prob_path}")
            paths['positive_probability_distribution'] = pos_prob_path
        
        # 5.2 Negative sample probability distribution
        if negative_probs:
            plt.figure(figsize=(12, 7))
            neg_prob_counts, _ = np.histogram(negative_probs, bins=prob_bins)
            plt.plot(prob_bin_centers, neg_prob_counts, 'o-', color='red', linewidth=2)
            plt.axvline(x=BINARY_THRESHOLD, color='blue', linestyle='--', 
                       label=f'Threshold ({BINARY_THRESHOLD})')
            plt.title(f'{safe_dataset} - {category} Negative Sample Probability Distribution')
            plt.xlabel('Probability')
            plt.ylabel('Count')
            plt.legend(['Negative (Without Helmet)', f'Threshold ({BINARY_THRESHOLD})'])
            plt.grid(True)
            plt.xlim(0, 1)
            plt.ylim(bottom=0)
            
            neg_prob_path = f'result/picture/{safe_dataset}_{category}_{safe_model}_{safe_prompt}_negative_probability_distribution.png'
            plt.savefig(neg_prob_path)
            plt.close()
            print(f"Negative sample probability distribution chart saved to: {neg_prob_path}")
            paths['negative_probability_distribution'] = neg_prob_path
            
        return paths
    
    return None 