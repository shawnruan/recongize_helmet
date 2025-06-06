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
        
        # Create scatter plot with scores
        plt.figure(figsize=(12, 7))
        
        # Define jitter range - full width of the category band
        jitter_range = 0.45  # Adjust to control vertical spread
        
        # Generate more uniform jitter for better visualization
        np.random.seed(42)  # Fixed seed for reproducibility
        
        # Generate uniform jitter across the entire range
        positive_jitter = np.random.uniform(-jitter_range, jitter_range, len(positive_scores))
        negative_jitter = np.random.uniform(-jitter_range, jitter_range, len(negative_scores))
        
        # Plot with jitter
        plt.scatter(
            positive_scores,
            1 + positive_jitter,
            color='green', alpha=0.7, label='Positive (With Helmet)'
        )
        plt.scatter(
            negative_scores,
            0 + negative_jitter,
            color='red', alpha=0.7, label='Negative (Without Helmet)'
        )
        
        # Add threshold line
        threshold_score = BINARY_THRESHOLD * 100
        plt.axvline(x=threshold_score, color='blue', linestyle='--', 
                   label=f'Threshold ({threshold_score})')
        
        # Set chart properties with comprehensive title
        plt.title(f'Dataset: {safe_dataset} - {category}\nModel: {model_name}\nPrompt: {safe_prompt}', fontsize=12)
        plt.xlabel('Score')
        plt.ylabel('Class')
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
        
        print(f"Score distribution scatter plot saved to: {scatter_path}")
        return {'score_scatter': scatter_path}
    
    return None 