import os
import re
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


def extract_scores_from_review(file_path):
    """
    Extract numerical scores from a review file.
    
    Returns:
        dict: Dictionary with score types and their values
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    scores = {}
    
    # Pattern 1: "## Soundness: 3" (with ##)
    # Pattern 2: "Soundness: 3" (without ##, standalone line)
    
    # Extract Soundness score
    soundness_match = re.search(r"(?:##\s*)?Soundness:\s*(\d+)", content, re.IGNORECASE)
    if soundness_match:
        scores['soundness'] = int(soundness_match.group(1))
    
    # Extract Presentation score
    presentation_match = re.search(r"(?:##\s*)?Presentation:\s*(\d+)", content, re.IGNORECASE)
    if presentation_match:
        scores['presentation'] = int(presentation_match.group(1))
    
    # Extract Contribution score
    contribution_match = re.search(r"(?:##\s*)?Contribution:\s*(\d+)", content, re.IGNORECASE)
    if contribution_match:
        scores['contribution'] = int(contribution_match.group(1))
    
    # Extract Rating score
    rating_match = re.search(r"(?:##\s*)?Rating:\s*\*?\*?(\d+)\*?\*?", content, re.IGNORECASE)
    if rating_match:
        scores['rating'] = int(rating_match.group(1))
    
    # Extract Confidence score
    confidence_match = re.search(r"(?:##\s*)?Confidence:\s*\*?\*?(\d+)\*?\*?", content, re.IGNORECASE)
    if confidence_match:
        scores['confidence'] = int(confidence_match.group(1))
    
    return scores


def analyze_reviews(output_dir, model_name=None, pdf_name=None):
    """
    Analyze review files in the output directory, optionally filtered by model and PDF name.
    
    Args:
        output_dir: Directory containing review text files
        model_name: Optional filter for specific model (e.g., "gpt-5-mini", "claude-haiku-4-5")
        pdf_name: Optional filter for specific PDF file (e.g., "a0kq0tJwwn")
    """
    # Collect all scores
    all_scores = defaultdict(list)
    
    # Get all .txt files
    all_files = sorted([f for f in os.listdir(output_dir) if f.endswith('.txt')])
    
    # Filter files based on model_name and pdf_name
    files = []
    for f in all_files:
        # File format: {model_name}_{pdf_name}_{attempt}.txt
        if model_name and not f.startswith(model_name):
            continue
        if pdf_name and f"_{pdf_name}_" not in f:
            continue
        files.append(f)
    
    if not files:
        print(f"No matching files found in {output_dir} for model={model_name}, pdf={pdf_name}")
        return None, None
    
    print(f"Found {len(files)} review files in {output_dir}")
    
    # Extract scores from each file
    for file_name in files:
        file_path = os.path.join(output_dir, file_name)
        scores = extract_scores_from_review(file_path)
        
        print(f"File: {file_name}")
        for score_type, value in scores.items():
            print(f"  {score_type}: {value}")
            all_scores[score_type].append(value)
        print()
    
    # Calculate statistics
    print("=" * 60)
    print("STATISTICS SUMMARY")
    print("=" * 60)
    
    # Prepare data for plotting
    score_types = ['soundness', 'presentation', 'contribution', 'rating', 'confidence']
    plot_data = {}
    
    for score_type in score_types:
        if score_type in all_scores and len(all_scores[score_type]) > 0:
            values = np.array(all_scores[score_type])
            plot_data[score_type] = values
            
            print(f"\n{score_type.upper()}:")
            print(f"  Count: {len(values)}")
            print(f"  Mean: {np.mean(values):.2f}")
            print(f"  Std: {np.std(values, ddof=1):.2f}")
            print(f"  Variance: {np.var(values, ddof=1):.2f}")
            print(f"  Min: {np.min(values)}")
            print(f"  Max: {np.max(values)}")
            print(f"  Median: {np.median(values):.1f}")
            print(f"  Distribution: {dict(zip(*np.unique(values, return_counts=True)))}")
    
    print("\n" + "=" * 60)
    
    # Create visualization
    if plot_data:
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(f'Review Scores Distribution Analysis - {output_dir}', fontsize=16, fontweight='bold')
        
        # Flatten axes for easier indexing
        axes = axes.flatten()
        
        for idx, score_type in enumerate(score_types):
            if score_type in plot_data:
                values = plot_data[score_type]
                ax = axes[idx]
                
                # Create histogram with distribution
                unique_vals, counts = np.unique(values, return_counts=True)
                ax.bar(unique_vals, counts, alpha=0.7, color='steelblue', edgecolor='black')
                
                # Add statistics text
                mean_val = np.mean(values)
                std_val = np.std(values, ddof=1)
                median_val = np.median(values)
                
                stats_text = f'Mean: {mean_val:.2f}\nStd: {std_val:.2f}\nMedian: {median_val:.1f}\nCount: {len(values)}'
                ax.text(0.95, 0.95, stats_text, transform=ax.transAxes, 
                       fontsize=9, verticalalignment='top', horizontalalignment='right',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
                
                # Formatting
                ax.set_xlabel('Score', fontsize=11)
                ax.set_ylabel('Frequency', fontsize=11)
                ax.set_title(f'{score_type.capitalize()} Distribution', fontsize=12, fontweight='bold')
                ax.grid(axis='y', alpha=0.3, linestyle='--')
                ax.set_xticks(unique_vals)
        
        # Hide the last subplot (6th position) since we only have 5 plots
        axes[5].set_visible(False)
        
        plt.tight_layout()
        
        # Create output directory for analysis images
        analyze_dir = "analyze_image"
        os.makedirs(analyze_dir, exist_ok=True)
        
        # Generate output filename based on model and pdf names
        if model_name and pdf_name:
            output_filename = f"{model_name}_{pdf_name}.png"
        elif model_name:
            output_filename = f"{model_name}_all.png"
        elif pdf_name:
            output_filename = f"all_models_{pdf_name}.png"
        else:
            output_filename = f"{os.path.basename(output_dir)}_all.png"
        
        output_file = os.path.join(analyze_dir, output_filename)
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"\nVisualization saved to: {output_file}")
        plt.close()
        
        return output_file, plot_data
    
    return None, None


if __name__ == "__main__":
    # Example 1: Analyze all files in output_gemini
    # analyze_reviews("output_gemini")
    
    # # Example 2: Analyze specific model in output_gemini
    # analyze_reviews("output_gemini", model_name="gemini-2.5-flash", pdf_name="a0kq0tJwwn")
    # analyze_reviews("output_gemini", model_name="gemini-2.5-flash-lite", pdf_name="a0kq0tJwwn")
    
    # # Example 3: Analyze all models for specific PDF
    # # analyze_reviews("output_gemini", pdf_name="a0kq0tJwwn")
    
    # # Example 4: Analyze other output directories
    # analyze_reviews("output_claude", model_name="claude-haiku-4-5", pdf_name="a0kq0tJwwn")
    
    
    # analyze_reviews("output_openai", model_name="gpt-5-mini", pdf_name="a0kq0tJwwn")
    analyze_reviews("output_openai", model_name="gpt-5", pdf_name="a0kq0tJwwn")
