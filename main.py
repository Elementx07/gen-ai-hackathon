import os
import streamlit as st
import json
import shutil
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Import the new website generator pipeline
from src.website_generator import generate_website_files
from src.ai_utils import call_gemini
from src.preview_server import show_preview_interface

PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = os.environ.get("MODEL", "gemini-2.5-flash")

if not PROJECT_ID:
    raise ValueError("PROJECT_ID environment variable not set")


# ---------- STREAMLIT UI ----------
st.set_page_config(layout="wide")
st.title("AI-Powered Artisan Website Generator")

   

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
        # Create progress bar and status text
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            from src.ai_utils import call_gemini_structured
            from src.models import SiteData
            from src.langchain_prompts import data_extraction_prompt, DATA_EXTRACTION_SYSTEM_PROMPT

             # Step 1: Call AI for structured JSON output using LangChain
            status_text.text("Step 1: Analyzing business description with LangChain...")
            progress_bar.progress(10)

            # Use LangChain structured output with Pydantic validation
            site_data_parsed = call_gemini_structured(
                prompt=data_extraction_prompt.format(description=desc),
                pydantic_model=SiteData,
                system_prompt=DATA_EXTRACTION_SYSTEM_PROMPT
            )
            
            # Convert Pydantic model to dict for JSON serialization
            site_data_dict = site_data_parsed.model_dump()
            
            # Save to file
            data_file = Path("generated_website/src/data/products.json")
            data_file.parent.mkdir(parents=True, exist_ok=True)
            with open(data_file, "w", encoding="utf-8") as f:
                json.dump(site_data_dict, f, indent=2)

            # Step 4: Generate website files with detailed progress
            status_text.text("Step 2: Generating website components...")
            progress_bar.progress(20)
            
            def website_progress_callback(current_step, total_steps, step_description):
                # Map website generation progress from 80% to 95%
                base_progress = 80
                step_range = 15  # 15% allocated for website generation
                step_progress = (current_step / total_steps) * step_range
                new_progress = int(base_progress + step_progress)
                
                progress_bar.progress(new_progress)
                status_text.text(f"Step 4/5: {step_description}")
            
            output_dir = generate_website_files(
                site_data_raw=json.dumps(site_data_dict, indent=2),
                user_prompt=desc,
                output_path="generated_website",
                progress_callback=website_progress_callback
            )

            # Step 5: Complete
            status_text.text("Step 5/5: Finalizing website generation...")
            progress_bar.progress(100)
            
            # Clear progress indicators and show success
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"Website source code generated successfully ")
            st.balloons()



            output_dir = Path("generated_website")
            zip_path = Path("generated_website.zip")

            # Remove old zip if exists
            if zip_path.exists():
                zip_path.unlink()

            # Create a zip of the generated folder
            shutil.make_archive("generated_website", 'zip', output_dir)

            # Provide download button
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="Download Generated Website",
                    data=f,
                    file_name="generated_website.zip",
                    mime="application/zip"
                )


            st.header("Next Steps: Build")
            st.code(f"""
                cd {output_dir}
                npm install
                npm run dev
                """, language="bash")

        except Exception as e:
            # Clear progress indicators on error
            progress_bar.empty()
            status_text.empty()
            
            st.error(f"An error occurred during code generation: {e}")
            st.exception(e)

if Path("generated_website").exists():
    st.markdown("---")
    show_preview_interface()
