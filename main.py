import os
import streamlit as st
import subprocess  # For running 'which gcloud'
import json
import re
from pathlib import Path
from dotenv import load_dotenv

# Import the new website generator pipeline
from src.website_generator import generate_website_files
from src.ai_utils import call_gemini

PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = os.environ.get("MODEL", "gemini-2.5")

if not PROJECT_ID:
    raise ValueError("PROJECT_ID environment variable not set")

# --- Helper to get gcloud path ---
def get_gcloud_path():
    """Finds the path to the gcloud executable."""
    try:
        result = subprocess.run(
            "which gcloud",
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        path = result.stdout.strip()
        if path and os.path.exists(path):
            return path
    except subprocess.CalledProcessError:
        pass

    try:
        home_dir = os.path.expanduser("~")
        default_path = os.path.join(home_dir, "google-cloud-sdk", "bin", "gcloud")
        if os.path.exists(default_path):
            return default_path
    except Exception:
        pass

    return None

# ---------- STREAMLIT UI ----------
st.set_page_config(layout="wide")
st.title("AI-Powered Artisan Website Generator ahahahhah")

with st.sidebar:
    st.header("Configuration")
    PROJECT_ID = os.getenv("PROJECT_ID")
    st.text_input("Google Cloud Project ID", value=PROJECT_ID, disabled=True)
    st.info("Ensure your Google Cloud Project ID is set in the .env file.")

    st.header("Deployment Tools Check")
    gcloud_path = get_gcloud_path()
    if gcloud_path:
        st.success(f"gcloud CLI found at: {gcloud_path}")
    else:
        st.error("gcloud CLI not found. Please install and configure it.")
        st.markdown("[Install gcloud CLI](https://cloud.google.com/sdk/docs/install)")

desc = st.text_area(
    "Describe your artisan business and products:",
    height=200,
    placeholder="Example: 'I am a potter named Sarah. I make unique, handmade ceramic mugs and bowls. "
                "My style is rustic and earthy. I have 5 types of mugs (forest green, ocean blue, desert sand) "
                "and 3 types of bowls (small, medium, large). Mugs are $25, bowls are $40. I also do custom orders. "
                "Contact me at sarah@pottery.com.'"
)

if st.button("Generate Website Files"):
    if not desc.strip():
        st.error("Please provide a description for your business.")
    elif not os.getenv("PROJECT_ID"):
        st.error("Please set your Google Cloud Project ID in environment variables.")
    else:
        with st.spinner("Generating website source code... This may take a minute."):
            try:
                from src.ai_utils import call_gemini
                from src.prompts import DATA_EXTRACTION_PROMPT

                # Call AI for JSON output
                site_data_raw = call_gemini(
                    prompt=DATA_EXTRACTION_PROMPT.format(description=desc),
                    system_prompt="Return strictly valid JSON. Include all requested fields completely."
                )
                # Debug: show raw output
                st.subheader("Raw AI Output")
                st.code(site_data_raw, language="json")

                # Remove Markdown/code fences and extra whitespace
                # Remove common AI prefixes and markdown/code fences
                cleaned_output = site_data_raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
                #display cleaned output for debugging
                st.subheader("Extracted JSON Data")
                st.code(cleaned_output, language="json") 
                match = re.search(r"\{.*\}", cleaned_output, re.S)
                if not match:
                    raise ValueError("No JSON object found")
                site_data_parsed = json.loads(match.group(0))

                # Save JSON to products.json
                data_file = Path("generated_website/src/data/products.json")
                data_file.parent.mkdir(parents=True, exist_ok=True)
                with open(data_file, "w", encoding="utf-8") as f:
                    json.dump(site_data_parsed, f, indent=2)

                # Generate website
                output_dir = generate_website_files(
                    site_data_raw=json.dumps(site_data_parsed, indent=2),
                    user_prompt=desc,
                    output_path="generated_website"
                )

                st.success(f"Website source code generated successfully in the '{output_dir}' directory!")
                st.balloons()

                st.header("Next Steps: Build and Deploy")
                st.code(f"""
cd {output_dir}
npm install
npm run dev
gcloud app deploy
""", language="bash")

            except Exception as e:
                st.error(f"An error occurred during code generation: {e}")
                st.exception(e)
