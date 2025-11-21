
import anthropic
import base64
import os

# initi client


# # print all available models
# models_data = client.models.list().data
# # print(models)
# for model_data in models_data:
#     print(model_data)
# breakpoint()

def review_paper_claude(pdf_file_path: str, reviewer_guidance: str, user_prompt: str, model_name: str = "claude-sonnet-4-5") -> str:
    """
    Review a PDF paper using Claude API with base64 encoding.
    
    Args:
        pdf_file_path: Path to the PDF file to review
        reviewer_guidance: System guidance for the reviewer
        user_prompt: User prompt for the review
        model_name: Claude model to use (default: "claude-sonnet-4-5")
    
    Returns:
        The review text from the model
    """
    
    client = anthropic.Anthropic()
    
    # Load and encode PDF file to base64
    with open(pdf_file_path, "rb") as f:
        pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")
    
    # Send to Claude using base64 encoding
    message = client.messages.create(
        model=model_name,
        max_tokens=int(10 * 1024),
        system=reviewer_guidance,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_data
                        }
                    },
                    {
                        "type": "text",
                        "text": user_prompt
                    }
                ]
            }
        ],
    )
    
    return message.content[0].text


if __name__ == "__main__":

    # Example usage
    pdf_file_path = "/ssd2/zhizhou/workspace/openreviewer/openreview_dataset_creation/data/pdfs/a0kq0tJwwn.pdf"

    # Read reviewer guidance from file
    with open("reviewer_guidance.txt", "r") as f:
        reviewer_guidance = f.read()
        
    user_prompt = "Please provide a detailed review of this paper following the guidance above."

    # model_name = "claude-sonnet-4-5"
    model_name = "claude-haiku-4-5"
    pdf_name = pdf_file_path.split("/")[-1].rstrip(".pdf")
    output_dir = "output_claude"
    os.makedirs(output_dir, exist_ok=True)

    total_tries = 10
    for attempt in range(total_tries):
        print(f"{model_name} Attempt {attempt + 1} of {total_tries}")
        output_file_path = os.path.join(output_dir, f"{model_name}_{pdf_name}_{attempt}.txt")

        # Call the function
        review_text = review_paper_claude(pdf_file_path, reviewer_guidance, user_prompt, model_name=model_name)

        # save to text file
        with open(output_file_path, "w") as f:
            f.write(review_text)

