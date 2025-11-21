
import os
from google import genai
from google.genai import types


def review_paper_gemini(pdf_file_path: str, reviewer_guidance: str, user_prompt: str, model_name: str = "gemini-2.5-flash-lite") -> str:
    """
    Review a PDF paper using Google Gemini API.
    
    Args:
        pdf_file_path: Path to the PDF file to review
        reviewer_guidance: System guidance for the reviewer
        user_prompt: User prompt for the review
        model_name: Gemini model to use (default: "gemini-2.0-flash-exp")
    
    Returns:
        The review text from the model
    """
    client = genai.Client()
    
    # Read PDF file as bytes
    with open(pdf_file_path, "rb") as f:
        pdf_data = f.read()
    
    # Create content with system instruction, PDF, and user prompt
    response = client.models.generate_content(
        model=model_name,
        contents=[
            types.Part.from_bytes(
                data=pdf_data,
                mime_type='application/pdf',
            ),
            user_prompt
        ],
        config=types.GenerateContentConfig(
            system_instruction=reviewer_guidance,
            temperature=1.0,
        )
    )
    
    return response.text


if __name__ == "__main__":
    # Example usage
    pdf_file_path = "/ssd2/zhizhou/workspace/openreviewer/openreview_dataset_creation/data/pdfs/a0kq0tJwwn.pdf"

    # Read reviewer guidance from file
    with open("reviewer_guidance.txt", "r") as f:
        reviewer_guidance = f.read()

    user_prompt = "Please provide a detailed review of this paper following the guidance above."

    # model_name = "gemini-2.5-flash-lite"
    
    model_name = "gemini-2.5-flash"
    
    pdf_name = pdf_file_path.split("/")[-1].rstrip(".pdf")
    output_dir = "output_gemini"
    os.makedirs(output_dir, exist_ok=True)

    total_tries = 10
    for attempt in range(total_tries):
        print(f"{model_name} Attempt {attempt + 1} of {total_tries}")
        output_file_path = os.path.join(output_dir, f"{model_name}_{pdf_name}_{attempt}.txt")

        # Call the function
        review_text = review_paper_gemini(pdf_file_path, reviewer_guidance, user_prompt, model_name=model_name)

        # save to text file
        with open(output_file_path, "w") as f:
            f.write(review_text)
