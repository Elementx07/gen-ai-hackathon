import os
import base64
import io
from PIL import Image
import streamlit as st
from streamlit.components.v1 import html

import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Part

# ---------- CONFIG ----------11
PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
MODEL = os.getenv("MODEL")


# Init client for Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# ---------- GENERATION ----------
def generate_website(raw_description: str, images: list) -> str:
    """
    Ask the model to return a single HTML file with CSS and JS.
    """
    system = (
        "You are an expert web developer. You will be given a product description and a product image."
        "Your task is to generate a single HTML file for a beautiful, modern, and polished e-commerce storefront to sell this product."
        "The HTML file should include inline CSS and JavaScript for a complete, visually appealing, and functional prototype."
        "Use Material Design principles for the UI/UX. The layout should be responsive."
        "The image will be provided as a base64 encoded string. You should embed it in the HTML."
    )
    
    image_parts = [Part.from_data(data=base64.b64decode(img), mime_type="image/png") for img in images]

    prompt = f"Product description: {raw_description}"

    model = GenerativeModel(MODEL, system_instruction=system)
    resp = model.generate_content(
        [prompt] + image_parts,
        generation_config=GenerationConfig(
            max_output_tokens=8192,
            temperature=0.2,
        ),
    )

    return resp.text

# ---------- UTIL ----------
def file_to_base64(f) -> str:
    img = Image.open(f).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

# ---------- STREAMLIT UI ----------
st.set_page_config(layout="wide")
st.title("AI-Powered Storefront Generator (Streamlit + Vertex AI)")

with st.sidebar:
    st.header("Settings")
    model_input = st.text_input("Model", value=MODEL)
    st.info("Set GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT env vars before running.")

uploaded = st.file_uploader("Upload product images", type=["png","jpg","jpeg"], accept_multiple_files=True)
desc = st.text_area("Product description / artisan notes", height=160)
if st.button("Generate Website"):
    if not uploaded or not desc.strip():
        st.error("Upload at least one image and provide a description.")
    else:
        # images -> base64
        images_b64 = []
        st.subheader("Enhanced images (preview)")
        cols = st.columns(min(4, len(uploaded)))
        for i, f in enumerate(uploaded):
            b64 = file_to_base64(f)
            images_b64.append(b64)
            with cols[i % len(cols)]:
                st.image(f, use_column_width=True)

        st.info("Generating website (Vertex AI)...")
        try:
            website_html = generate_website(desc, images_b64)
            st.success("Website generated.")
        except Exception as e:
            st.error(f"Website generation failed: {e}")
            st.stop()

        st.subheader("Generated Website Preview")
        html(website_html, height=600, scrolling=True)

        # download export
        st.download_button(
            label="Download website HTML",
            data=website_html,
            file_name="storefront.html",
            mime="text/html",
        )