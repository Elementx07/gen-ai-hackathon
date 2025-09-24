import os
import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

class GenerationError(Exception):
    pass

def write_file_wrapper(file_path: Path, content: str):
    """Write content to file"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_code_from_string(text: str, language_hint: str = "tsx") -> str:
    """Extract code from AI response (dummy passthrough)"""
    return text.strip().removeprefix("```tsx").removeprefix("```").removesuffix("```").strip()

class WebsiteGenerator:
    def __init__(self, site_data_raw: str, user_prompt: str, output_path: Path, dry_run: bool = False, run_install: bool = True):
        self.site_data_raw = site_data_raw
        self.user_prompt = user_prompt
        self.output_path = output_path
        self.dry_run = dry_run
        self.run_install = run_install

    def _call_ai_with_retries(self, prompt: str, system_prompt: str) -> str:
        """Call AI with retry logic"""
        from src.ai_utils import call_gemini
        try:
            return call_gemini(prompt, system_prompt)
        except Exception as e:
            logger.warning(f"AI call failed: {e}. Retrying once...")
            return call_gemini(prompt, system_prompt)

    def _install_dependencies(self, output_path: str, run_install: bool = True):
        """Install project dependencies"""
        if not run_install:
            return
        os.system(f"cd {output_path} && npm install")

    def generate(self) -> str:
        # Save the raw AI site data
        data_dir = self.output_path / "src" / "data"
        write_file_wrapper(data_dir / "products.json", self.site_data_raw)

        # Lazy import to avoid circular issues
        from src.prompts import (
            REACT_COMPONENT_PROMPT,
            REACT_PAGE_PROMPT,
            LAYOUT_PROMPT,
            GLOBALS_CSS_PROMPT,
        )

        def generate_and_write(name: str, file_subpath: str, prompt_template: str, system_prompt: str, language_hint: str = "tsx", component_data: Dict = None):
            logger.info(f"Generating {name} -> {file_subpath}")
            full_prompt = prompt_template.format(
                site_data=self.site_data_raw,
                component_name=name,
                component_data=json.dumps(component_data or {}),
                description=self.user_prompt,
                design_system=json.dumps({}),
                page_name=name,
            )
            ai_resp = self._call_ai_with_retries(prompt=full_prompt, system_prompt=system_prompt)
            code = extract_code_from_string(ai_resp, language_hint)
            if not code:
                write_file_wrapper(self.output_path / (file_subpath + ".raw.txt"), ai_resp)
                return
            write_file_wrapper(self.output_path / file_subpath, code)

        # Components
        components = {
            "Navbar": "src/components/Navbar.tsx",
            "Footer": "src/components/Footer.tsx",
            "ProductCard": "src/components/ProductCard.tsx",
            "ContactForm": "src/components/ContactForm.tsx",
        }
        for name, path in components.items():
            generate_and_write(name, path, REACT_COMPONENT_PROMPT, "React component generator")

        # Pages
        pages = {
            "homepage": "src/app/page.tsx",
            "products": "src/app/products/page.tsx",
            "about": "src/app/about/page.tsx",
            "gallery": "src/app/gallery/page.tsx",
            "contact": "src/app/contact/page.tsx",
        }
        for name, path in pages.items():
            generate_and_write(name, path, REACT_PAGE_PROMPT, "Next.js page generator")

        # Layout and globals
        generate_and_write("RootLayout", "src/app/layout.tsx", LAYOUT_PROMPT, "Next.js layout generator")
        generate_and_write("GlobalsCSS", "src/app/globals.css", GLOBALS_CSS_PROMPT, "CSS globals generator", language_hint="css")

        if not self.dry_run:
            print(f"Website generated at: {self.output_path}")
            #   self._install_dependencies(str(self.output_path), run_install=self.run_install)

        return str(self.output_path)


def generate_website_files(site_data_raw: str, user_prompt: str, output_path: str, dry_run: bool = False, run_install: bool = True, progress_callback=None) -> str:
    """Generate website files with optional progress tracking."""
    
    # Define the steps for website generation
    total_steps = 6  # Adjust based on your actual steps
    current_step = 0
    
    def update_progress(description):
        nonlocal current_step
        current_step += 1
        if progress_callback:
            progress_callback(current_step, total_steps, description)
    
    try:
        generator = WebsiteGenerator(
            site_data_raw=site_data_raw,
            user_prompt=user_prompt,
            output_path=Path(output_path),
            dry_run=dry_run,
            run_install=run_install
        )
        
        # Step 1: Generate HTML files
        update_progress("Generating templates...")
        # Your HTML generation code here
        
        # Step 2: Generate CSS files
        update_progress("Creating stylesheets...")
        # Your CSS generation code here
        
        # Step 3: Generate JavaScript files
        update_progress("Building interactive components...")
        # Your JS generation code here
        
        # Step 4: Generate configuration files
        update_progress("Setting up project configuration...")
        # Your config generation code here
        
        # Step 5: Copy assets and dependencies
        update_progress("Creating Layout...")
        # Your asset copying code here
        
        # Step 6: Final cleanup
        update_progress("Finalizing project structure...")
        # Your cleanup code here
        
        return output_path
        
    except Exception as e:
        if progress_callback:
            progress_callback(current_step, total_steps, f"Error: {str(e)}")
        raise
