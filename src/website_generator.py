import os
import json
import re
import shutil # Using Python's built-in library for directory operations
from typing import Dict, Any, Optional

from src.ai_utils import call_gemini
import os
import json
import subprocess

from jinja2 import Environment, FileSystemLoader

from src.ai_utils import generate_response
from src.prompts import (
    DATA_EXTRACTION_PROMPT,
    REACT_COMPONENT_PROMPT,
    REACT_PAGE_PROMPT,
    LAYOUT_PROMPT,
    GLOBALS_CSS_PROMPT,
)


# --- Helper Functions (run_shell_command_wrapper is removed) ---

def extract_json_from_string(s: str) -> Optional[Dict[str, Any]]:
    """Finds, parses, and returns the first JSON object within a string."""
    match = re.search(r"```json\s*(.*?)\s*```", s, re.DOTALL)
    json_str = ""
    if match:
        json_str = match.group(1).strip()
    else:
        start = s.find('{')
        end = s.rfind('}')
        if start != -1 and end != -1:
            json_str = s[start:end+1].strip()

    if not json_str:
        print("--- Warning: Could not find JSON in string ---")
        return None
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"--- Warning: Failed to decode JSON ---")
        print(f"Error: {e}")
        print(f"String: {json_str[:500]}...")
        return None

def extract_code_from_string(s: str, language: str) -> str:
    """Extracts a code block for a given language from a string."""
    pattern = re.compile(r"```" + re.escape(language) + r"\s*(.*?)\s*```", re.DOTALL)
    match = pattern.search(s)
    if match:
        return match.group(1).strip()
    # Fallback for when the AI forgets the language tag
    return re.sub(r"```[a-zA-Z]*", "", s).replace("```", "").strip()


def write_file_wrapper(file_path: str, content: str):
    """Creates directories and writes content to a file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)
        print(f"--- Wrote File: {file_path} ---")
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")
        raise

# --- New Helper to create standard config files ---

def create_scaffolding_files(base_dir: str, project_name: str):
    """Creates the necessary config files for a Next.js project."""
    files = {
        "package.json": {
            "name": project_name,
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": {
                "react": "^18",
                "react-dom": "^18",
                "next": "14.2.4"
            },
            "devDependencies": {
                "typescript": "^5",
                "@types/node": "^20",
                "@types/react": "^18",
                "@types/react-dom": "^18",
                "postcss": "^8",
                "tailwindcss": "^3.4.1",
                "autoprefixer": "^10.4.19",
                "eslint": "^8",
                "eslint-config-next": "14.2.4"
            }
        },
        "tsconfig.json": {
            "compilerOptions": {
                "lib": ["dom", "dom.iterable", "esnext"],
                "allowJs": True,
                "skipLibCheck": True,
                "strict": True,
                "noEmit": True,
                "esModuleInterop": True,
                "module": "esnext",
                "moduleResolution": "bundler",
                "resolveJsonModule": True,
                "isolatedModules": True,
                "jsx": "preserve",
                "incremental": True,
                "plugins": [{"name": "next"}],
                "paths": {"@/*": ["./src/*"]}
            },
            "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
            "exclude": ["node_modules"]
        },
        "next.config.mjs": """
/** @type {import('next').NextConfig} */
const nextConfig = {};
export default nextConfig;
""",
        "postcss.config.mjs": """
/** @type {import('postcss-load-config').Config} */
const config = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
export default config;
"""
    }
    for filename, content in files.items():
        path = os.path.join(base_dir, filename)
        if isinstance(content, dict):
            write_file_wrapper(path, json.dumps(content, indent=2))
        else:
            write_file_wrapper(path, content)

# --- Main Orchestration Function (Refactored) ---

def _install_dependencies(output_dir: str):
    package_json_path = os.path.join(output_dir, 'package.json')

    # Read existing package.json
    with open(package_json_path, 'r') as f:
        package_json = json.load(f)

    # Add common dependencies if not already present
    if 'dependencies' not in package_json:
        package_json['dependencies'] = {}
    if 'devDependencies' not in package_json: # Corrected: was 'not not in'
        package_json['devDependencies'] = {}

    # Hardcoded dependencies based on common Next.js project needs and our errors
    common_dependencies = {
        "react": "^18",
        "react-dom": "^18",
        "next": "^14",
        "@next/font": "latest", # Use latest for @next/font
        "tailwindcss": "^3",
        "autoprefixer": "^10",
        "postcss": "^8",
        "lucide-react": "^0.303.0" # Added due to previous error
    }

    for dep, version in common_dependencies.items():
        if dep not in package_json['dependencies']:
            package_json['dependencies'][dep] = version

    # Write updated package.json
    with open(package_json_path, 'w') as f:
        json.dump(package_json, f, indent=2)

    print(f"Installing dependencies in {output_dir}...")
    try:
        subprocess.run(['npm', 'install'], cwd=output_dir, check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        print(e.stdout.decode())
        print(e.stderr.decode())

def generate_website_files(user_prompt: str) -> str:
    """
    Generates all source files for a Next.js website based on a user prompt.
    """
    generated_website_dir = "generated_website"

    # --- 1. Set up Project Directory ---
    print("--- Step 1: Setting up Project Directory ---")
    if os.path.exists(generated_website_dir):
        shutil.rmtree(generated_website_dir)
    os.makedirs(os.path.join(generated_website_dir, "src", "app"), exist_ok=True)
    
    create_scaffolding_files(generated_website_dir, "artisan-website")

    # --- 2. AI Data Analyst: Extract Structured Data ---
    print("\n--- Step 2: AI Data Analyst - Extracting Structured Data ---")
    site_data_raw = call_gemini(
        prompt=DATA_EXTRACTION_PROMPT.format(description=user_prompt),
        system_prompt="You are a data analyst extracting structured data from a user prompt into JSON."
    )
    site_data = extract_json_from_string(site_data_raw)
    if not site_data:
        raise ValueError("AI failed to return valid JSON data for the website.")
    
    # Write the data to a file for the components to use
    data_dir = os.path.join(generated_website_dir, "src", "data")
    write_file_wrapper(os.path.join(data_dir, "products.json"), json.dumps(site_data, indent=2))
    print("Site data saved to src/data/products.json")

    # --- 3. AI React Developer: Generate Components and Pages ---
    print("\n--- Step 3: AI React Developer - Generating Files ---")
    
    def generate_and_write_code(
        component_or_page_name: str,
        file_sub_path: str,
        prompt_template: str,
        system_prompt: str,
        component_data: Dict = None
    ):
        print(f"Generating {component_or_page_name}...")
        full_prompt = prompt_template.format(
            site_data=json.dumps(site_data),
            component_name=component_or_page_name,
            page_name=component_or_page_name, # For page prompts
            design_system=json.dumps(site_data.get("designSystem", {})), # For CSS prompt
            component_data=json.dumps(component_data or {})
        )
        code_raw = call_gemini(prompt=full_prompt, system_prompt=system_prompt)
        code_content = extract_code_from_string(code_raw, "tsx") # Assuming tsx for most
        if not code_content and "css" in file_sub_path:
             code_content = extract_code_from_string(code_raw, "css")

        write_file_wrapper(os.path.join(generated_website_dir, file_sub_path), code_content)
        print(f"Generated {component_or_page_name} and saved to {file_sub_path}.")

    # Generate Components
    components_to_generate = {
        "Navbar": "src/components/Navbar.tsx",
        "Footer": "src/components/Footer.tsx",
        "ProductCard": "src/components/ProductCard.tsx",
        "ContactForm": "src/components/ContactForm.tsx",
    }
    for name, path in components_to_generate.items():
        generate_and_write_code(
            name, path, REACT_COMPONENT_PROMPT,
            "You are an expert React and Tailwind CSS developer creating a reusable component."
        )

    # Generate Pages
    pages_to_generate = {
        "homepage": "src/app/page.tsx",
        "products": "src/app/products/page.tsx",
        "about": "src/app/about/page.tsx",
        "gallery": "src/app/gallery/page.tsx",
        "contact": "src/app/contact/page.tsx",
    }
    for name, path in pages_to_generate.items():
        # Create parent directory for page if it doesn't exist
        os.makedirs(os.path.dirname(os.path.join(generated_website_dir, path)), exist_ok=True)
        generate_and_write_code(
            name, path, REACT_PAGE_PROMPT,
            "You are an expert Next.js developer creating a page for the App Router."
        )

    # Generate Layout and Global CSS
    generate_and_write_code(
        "RootLayout", "src/app/layout.tsx", LAYOUT_PROMPT,
        "You are an expert Next.js developer creating the root layout."
    )
    generate_and_write_code(
        "GlobalsCSS", "src/app/globals.css", GLOBALS_CSS_PROMPT,
        "You are a CSS specialist setting up globals.css for Tailwind."
    )

    # --- 4. Return output directory ---
    print("\n--- Code Generation Complete ---")
    print(f"All files have been generated in the '{generated_website_dir}' directory.")
    
    _install_dependencies(generated_website_dir)
    
    return generated_website_dir