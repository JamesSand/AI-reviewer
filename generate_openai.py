import base64
import os
from openai import OpenAI


def review_paper_openai(pdf_file_path: str, reviewer_guidance: str, user_prompt: str, model_name: str = "gpt-5-mini") -> str:
    """
    Review a PDF paper using OpenAI API with base64 encoding.
    
    Args:
        pdf_file_path: Path to the PDF file to review
        reviewer_guidance: System guidance for the reviewer
        user_prompt: User prompt for the review
        model_name: OpenAI model to use (default: "gpt-5-mini")
    
    Returns:
        The review text from the model
    """
    client = OpenAI()
    
    # Extract pdf name from pdf file path
    pdf_paper_name = pdf_file_path.split("/")[-1]
    
    # Read and encode PDF file to base64
    with open(pdf_file_path, "rb") as f:
        data = f.read()
    
    base64_string = base64.b64encode(data).decode("utf-8")
    
    response = client.responses.create(
        model=model_name,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": reviewer_guidance,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_file",
                        "filename": pdf_paper_name,
                        "file_data": f"data:application/pdf;base64,{base64_string}",
                    },
                    {
                        "type": "input_text",
                        "text": user_prompt,
                    },
                ]
            }
        ]
    )
    
    return response.output_text


if __name__ == "__main__":

    # Example usage
    pdf_file_path = "/ssd2/zhizhou/workspace/openreviewer/openreview_dataset_creation/data/pdfs/a0kq0tJwwn.pdf"

    # Read reviewer guidance from file
    with open("reviewer_guidance.txt", "r") as f:
        reviewer_guidance = f.read()

    user_prompt = "Please provide a detailed review of this paper following the guidance above."

    # model_name = "gpt-5-mini"
    
    model_name = "gpt-5"
    pdf_name = pdf_file_path.split("/")[-1].rstrip(".pdf")
    output_dir = "output_openai"
    os.makedirs(output_dir, exist_ok=True)

    total_tries = 10
    for attempt in range(total_tries):
        print(f"{model_name} Attempt {attempt + 1} of {total_tries}")
        output_file_path = os.path.join(output_dir, f"{model_name}_{pdf_name}_{attempt}.txt")

        # Call the function
        review_text = review_paper_openai(pdf_file_path, reviewer_guidance, user_prompt, model_name=model_name)

        # print(review_text)

        # save to text file
        with open(output_file_path, "w") as f:
            f.write(review_text)

