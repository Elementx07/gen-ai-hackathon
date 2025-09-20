import os
import vertexai
from dotenv import load_dotenv
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Load environment variables from .env file
load_dotenv()

# Initialize Vertex AI client once
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
MODEL = os.getenv("MODEL")

# Check if the project ID is set
if not PROJECT_ID or PROJECT_ID == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
    raise ValueError("PROJECT_ID not found or not set in .env file. Please set it to your Google Cloud Project ID.")

vertexai.init(project=PROJECT_ID, location=LOCATION)

def call_gemini(prompt: str, system_prompt: str = None, max_output_tokens: int = 8192, temperature: float = 0.4) -> str:
    """
    Calls the Gemini model with a given prompt and system instruction.
    """
    model = GenerativeModel(MODEL, system_instruction=system_prompt)
    resp = model.generate_content(
        [prompt],
        generation_config=GenerationConfig(
            max_output_tokens=max_output_tokens,
            temperature=temperature,
        ),
    )
    return resp.text
