import os
import streamlit as st
from streamlit.components.v1 import html
import subprocess # For running 'which gcloud'
from dotenv import load_dotenv

# Import the new website generator pipeline
from src.website_generator import generate_website_files


load_dotenv()
# --- Helper to get gcloud path ---
def get_gcloud_path():
    """
    Finds the path to the gcloud executable.
    Checks common locations if 'which' command fails.
    """
    # 1. Try 'which' command first (for standard PATH)
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
        pass # Not found in PATH, try next method

    # 2. Check default installation location in user's home directory
    try:
        home_dir = os.path.expanduser("~")
        default_path = os.path.join(home_dir, "google-cloud-sdk", "bin", "gcloud")
        if os.path.exists(default_path):
            return default_path
    except Exception:
        pass # Could not check default path

    # 3. If not found, return None
    return None

# ---------- STREAMLIT UI ----------
st.set_page_config(layout="wide")
st.title("AI-Powered Artisan Website Generator")

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
    
    # Note: Docker daemon check is handled by the deploy command itself now.

desc = st.text_area(
    "Describe your artisan business and products:",
    height=200,
    placeholder="Example: 'I am a potter named Sarah. I make unique, handmade ceramic mugs and bowls. My style is rustic and earthy. I have 5 types of mugs (forest green, ocean blue, desert sand) and 3 types of bowls (small, medium, large). Mugs are $25, bowls are $40. I also do custom orders. Contact me at sarah@pottery.com.'"
)

if st.button("Generate Website Files"):
    if not desc.strip():
        st.error("Please provide a description for your business.")
    elif not os.getenv("PROJECT_ID"):
        st.error("Please set your Google Cloud Project ID in the .env file.")
    else:
        with st.spinner("Generating website source code... This may take a minute."):
            try:
                # 1. Call AI to extract site data
                from src.ai_utils import call_gemini
                from src.prompts import DATA_EXTRACTION_PROMPT
                site_data_raw = call_gemini(
                    prompt=DATA_EXTRACTION_PROMPT,
                    system_prompt="You are a data analyst extracting structured JSON from text."
                )

                # 3. Generate website
                output_dir = generate_website_files(
                    site_data_raw=site_data_raw,
                    user_prompt=desc,
                    output_path="generated_website"
                )

                st.success(f"Website source code generated successfully in the '{output_dir}' directory!")
                st.balloons()

                st.header("Next Steps: Build and Deploy")
                st.markdown("Open your terminal and run the following commands one by one:")
                st.code(f"""
cd {output_dir}
npm install
npm run dev
gcloud app deploy
                """, language="bash")

            except Exception as e:
                st.error(f"An error occurred during code generation: {e}")
                st.exception(e)
