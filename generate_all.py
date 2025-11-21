from generate_claude import review_paper_claude
from generate_gemini import review_paper_gemini
from generate_openai import review_paper_openai
import os
import argparse


def generate_reviews_for_paper(pdf_file_path: str, reviewer_guidance_path: str = "reviewer_guidance.txt", 
                                total_tries: int = 10, output_base_dir: str = "output"):
    """
    Generate reviews for a single paper using all three APIs (OpenAI, Claude, Gemini).
    Each API is called 10 times.
    
    Args:
        pdf_file_path: Path to the PDF file to review
        reviewer_guidance_path: Path to the reviewer guidance text file
        total_tries: Number of times to call each API (default: 10)
        output_base_dir: Base directory for all outputs (default: "output")
    """
    # Read reviewer guidance from file
    with open(reviewer_guidance_path, "r") as f:
        reviewer_guidance = f.read()
    
    user_prompt = "Please provide a detailed review of this paper following the guidance above."
    
    # Extract PDF name without extension
    pdf_name = os.path.basename(pdf_file_path).rstrip(".pdf")
    
    # Define models for each API
    api_configs = [
        {
            "api_name": "openai",
            "models": ["gpt-5", "gpt-5-mini"],
            "function": review_paper_openai,
            "output_dir": os.path.join(output_base_dir, "output_openai")
        },
        {
            "api_name": "claude",
            "models": ["claude-sonnet-4-5", "claude-haiku-4-5"],
            "function": review_paper_claude,
            "output_dir": os.path.join(output_base_dir, "output_claude")
        },
        {
            "api_name": "gemini",
            "models": ["gemini-2.5-flash", "gemini-2.5-flash-lite"],
            "function": review_paper_gemini,
            "output_dir": os.path.join(output_base_dir, "output_gemini")
        }
    ]
    
    # Process each API
    for api_config in api_configs:
        api_name = api_config["api_name"]
        models = api_config["models"]
        review_function = api_config["function"]
        output_dir = api_config["output_dir"]
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n{'='*60}")
        print(f"Processing {api_name.upper()} API")
        print(f"{'='*60}")
        
        # Process each model
        for model_name in models:
            print(f"\n[{api_name.upper()}] Using model: {model_name}")
            
            # Generate reviews (10 times per model)
            for attempt in range(total_tries):
                try:
                    print(f"  Attempt {attempt + 1}/{total_tries}...", end=" ")
                    
                    output_file_path = os.path.join(output_dir, f"{model_name}_{pdf_name}_{attempt}.txt")
                    
                    # Skip if file already exists
                    if os.path.exists(output_file_path):
                        print("Already exists, skipping.")
                        continue
                    
                    # Call the review function
                    review_text = review_function(pdf_file_path, reviewer_guidance, user_prompt, model_name=model_name)
                    
                    # Save to text file
                    with open(output_file_path, "w") as f:
                        f.write(review_text)
                    
                    print("Done.")
                    
                except Exception as e:
                    print(f"Error: {e}")
                    continue
        
        print(f"\n[{api_name.upper()}] Completed!")
    
    print(f"\n{'='*60}")
    print("All reviews generated successfully!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate reviews for a paper using multiple AI models")
    parser.add_argument("--pdf_path", type=str, help="Path to the PDF file")
    parser.add_argument("--guidance", type=str, default="reviewer_guidance.txt", 
                        help="Path to reviewer guidance file (default: reviewer_guidance.txt)")
    parser.add_argument("--tries", type=int, default=10, 
                        help="Number of times to call each model (default: 10)")
    parser.add_argument("--output", type=str, default="output", 
                        help="Base output directory (default: output)")
    
    args = parser.parse_args()
    
    # Check if PDF file exists
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file not found: {args.pdf_path}")
        exit(1)
    
    # Check if guidance file exists
    if not os.path.exists(args.guidance):
        print(f"Error: Reviewer guidance file not found: {args.guidance}")
        exit(1)
    
    print(f"Starting review generation for: {args.pdf_path}")
    print(f"Reviewer guidance: {args.guidance}")
    print(f"Attempts per model: {args.tries}")
    print(f"Output directory: {args.output}")
    
    generate_reviews_for_paper(args.pdf_path, args.guidance, args.tries, args.output)






