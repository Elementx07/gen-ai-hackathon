import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Callable
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)

class GenerationError(Exception):
    pass

def write_file_wrapper(file_path: Path, content: str):
    """Write content to file"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_code_from_string(text: str, language_hint: str = "tsx") -> str:
    """Extract code from AI response, removing markdown fences"""
    cleaned = text.strip()
    # Remove various markdown fence formats
    for fence in ["```tsx", "```typescript", "```jsx", "```javascript", "```css", "```"]:
        cleaned = cleaned.removeprefix(fence)
    cleaned = cleaned.removesuffix("```").strip()
    return cleaned

class WebsiteGenerator:
    def __init__(
        self, 
        site_data_raw: str, 
        user_prompt: str, 
        output_path: Path, 
        dry_run: bool = False, 
        run_install: bool = True,
        progress_callback: Optional[Callable] = None
    ):
        self.site_data_raw = site_data_raw
        self.user_prompt = user_prompt
        self.output_path = output_path
        self.dry_run = dry_run
        self.run_install = run_install
        self.progress_callback = progress_callback
        self.current_step = 0
        self.total_steps = 12  # Total number of generation steps

    def _update_progress(self, description: str):
        """Update progress if callback is provided"""
        self.current_step += 1
        if self.progress_callback:
            self.progress_callback(self.current_step, self.total_steps, description)

    def _call_ai_with_retries(self, prompt: str, system_prompt: str) -> str:
        """Call AI with retry logic using LangChain"""
        from src.ai_utils import call_gemini
        try:
            return call_gemini(prompt, system_prompt)
        except Exception as e:
            logger.warning(f"AI call failed: {e}. Retrying once...")
            return call_gemini(prompt, system_prompt)

    def _call_ai_with_chain(self, chain, input_data: Dict) -> str:
        """Call AI using a LangChain chain with retry logic"""
        try:
            return chain.invoke(input_data)
        except Exception as e:
            logger.warning(f"Chain call failed: {e}. Retrying once...")
            return chain.invoke(input_data)

    def _install_dependencies(self, output_path: str, run_install: bool = True):
        """Install project dependencies"""
        if not run_install:
            return
        os.system(f"cd {output_path} && npm install")

    def generate(self) -> str:
        """Generate the complete website using LangChain"""
        # Save the raw AI site data
        data_dir = self.output_path / "src" / "data"
        write_file_wrapper(data_dir / "products.json", self.site_data_raw)
        self._update_progress("Saved site data")

        # Import LangChain prompts and create chains
        from src.langchain_prompts import (
            component_generation_prompt,
            page_generation_prompt,
            layout_generation_prompt,
            css_generation_prompt,
            COMPONENT_SYSTEM_PROMPT,
            PAGE_SYSTEM_PROMPT,
            LAYOUT_SYSTEM_PROMPT,
            CSS_SYSTEM_PROMPT
        )
        from src.ai_utils import create_chain

        # Create reusable chains
        component_chain = create_chain(
            component_generation_prompt.template,
            COMPONENT_SYSTEM_PROMPT,
            StrOutputParser()
        )
        
        page_chain = create_chain(
            page_generation_prompt.template,
            PAGE_SYSTEM_PROMPT,
            StrOutputParser()
        )
        
        layout_chain = create_chain(
            layout_generation_prompt.template,
            LAYOUT_SYSTEM_PROMPT,
            StrOutputParser()
        )
        
        css_chain = create_chain(
            css_generation_prompt.template,
            CSS_SYSTEM_PROMPT,
            StrOutputParser()
        )

        def generate_and_write_with_chain(
            name: str, 
            file_subpath: str, 
            chain, 
            input_data: Dict,
            language_hint: str = "tsx"
        ):
            """Generate code using a LangChain chain and write to file"""
            logger.info(f"Generating {name} -> {file_subpath}")
            self._update_progress(f"Generating {name}")
            
            try:
                ai_resp = self._call_ai_with_chain(chain, input_data)
                code = extract_code_from_string(ai_resp, language_hint)
                if not code:
                    write_file_wrapper(self.output_path / (file_subpath + ".raw.txt"), ai_resp)
                    logger.warning(f"Empty code for {name}, saved raw response")
                    return
                write_file_wrapper(self.output_path / file_subpath, code)
            except Exception as e:
                logger.error(f"Error generating {name}: {e}")
                raise GenerationError(f"Failed to generate {name}: {e}")

        # Components
        components = {
            "Navbar": "src/components/Navbar.tsx",
            "Footer": "src/components/Footer.tsx",
            "ProductCard": "src/components/ProductCard.tsx",
            "ContactForm": "src/components/ContactForm.tsx",
        }
        
        for name, path in components.items():
            generate_and_write_with_chain(
                name, 
                path, 
                component_chain,
                {"component_name": name, "site_data": self.site_data_raw}
            )

        # Pages
        pages = {
            "homepage": "src/app/page.tsx",
            "products": "src/app/products/page.tsx",
            "about": "src/app/about/page.tsx",
            "gallery": "src/app/gallery/page.tsx",
            "contact": "src/app/contact/page.tsx",
        }
        
        for name, path in pages.items():
            generate_and_write_with_chain(
                name,
                path,
                page_chain,
                {"page_name": name, "site_data": self.site_data_raw}
            )

        # Layout
        generate_and_write_with_chain(
            "RootLayout",
            "src/app/layout.tsx",
            layout_chain,
            {"site_data": self.site_data_raw}
        )

        # Globals CSS
        generate_and_write_with_chain(
            "GlobalsCSS",
            "src/app/globals.css",
            css_chain,
            {"design_system": self.site_data_raw},
            language_hint="css"
        )

        if not self.dry_run:
            print(f"Website generated at: {self.output_path}")

        return str(self.output_path)


def generate_website_files(
    site_data_raw: str, 
    user_prompt: str, 
    output_path: str, 
    dry_run: bool = False, 
    run_install: bool = True, 
    progress_callback: Optional[Callable] = None
) -> str:
    """
    Generate website files using LangChain with optional progress tracking.
    
    Args:
        site_data_raw: JSON string of site data
        user_prompt: Original user description
        output_path: Output directory path
        dry_run: If True, don't actually generate files
        run_install: If True, run npm install
        progress_callback: Optional callback for progress updates
        
    Returns:
        Path to generated website
    """
    try:
        generator = WebsiteGenerator(
            site_data_raw=site_data_raw,
            user_prompt=user_prompt,
            output_path=Path(output_path),
            dry_run=dry_run,
            run_install=run_install,
            progress_callback=progress_callback
        )
        
        return generator.generate()
        
    except Exception as e:
        logger.error(f"Website generation failed: {e}")
        if progress_callback:
            progress_callback(0, 1, f"Error: {str(e)}")
        raise
