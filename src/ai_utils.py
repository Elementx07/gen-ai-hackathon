import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = os.environ.get("MODEL", "gemini-2.5-pro")

if not PROJECT_ID:
    raise ValueError("PROJECT_ID environment variable not set")
if not PROJECT_ID or PROJECT_ID == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
    raise ValueError("PROJECT_ID not set. Set it in your .env file.")

client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

def call_gemini(prompt: str, system_prompt: str = None, max_output_tokens: int = 8024, temperature: float = 0.4) -> str:
    full_prompt = f"{system_prompt}\n{prompt}" if system_prompt else prompt

    generation_config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=[{"text": full_prompt}],
        config=generation_config
    )
    return response.text
