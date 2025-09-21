# prompts.py

DATA_EXTRACTION_PROMPT = '''
You are a data analyst. 
A local artisan has provided a description of their business.
Extract structured data and return it as a single valid JSON object only.

Schema (required top-level keys):
- artisanInfo: object { name: string, story: string, contact: string }
- products: array of objects { id: string, name: string, description: string, price: string, imageUrl: string }
- galleryItems: array of objects { id: string, name: string, description: string, imageUrl: string }
- designSystem: object { colorPalette: object, typography: object, brandPersona: string }

Constraints:
- Return valid JSON only.
- Do not add explanations, markdown, or extra text.
- Do not include comments.
'''


REACT_COMPONENT_PROMPT = '''
You are an expert React + TypeScript + Tailwind developer.

Constraints:
- Use Next.js App Router conventions.
- If you use hooks, add "use client" at the top.
- Use Next.js <Image> from "next/image" and <Link> from "next/link".
- Define explicit prop types (interface).
- Only import from "next/*", "@/components", or "@/data".
- Do not use any external UI libraries (e.g., shadcn, MUI, Bootstrap).
- Code must be a single valid .tsx file.
- No markdown, no comments, no explanation outside the code.

Input:
{site_data}
Component: {component_name}
Component data: {component_data}
'''


REACT_PAGE_PROMPT = '''
You are an expert Next.js developer.

Constraints:
- Generate a single .tsx file for a page in the App Router.
- Import components only from "@/components".
- Load site data only from "@/data/products.json".
- Do not use external libraries beyond Next.js, React, and Tailwind.
- Return only valid TypeScript/TSX code.
- No comments, no markdown, no extra text.

Input:
{site_data}
Page: {page_name}
'''


LAYOUT_PROMPT = '''
You are an expert Next.js developer.

Constraints:
- Follow App Router layout conventions (layout.tsx).
- Import Google Fonts using next/font/google based on designSystem.typography.
- Import "@/components/Navbar" and "@/components/Footer".
- Pass artisanInfo and designSystem as props to these components.
- Set metadata.title = artisanInfo.name and metadata.description = artisanInfo.story.
- Export RootLayout.
- Return only valid TSX code, no comments or extra text.

Input:
{site_data}
'''


GLOBALS_CSS_PROMPT = '''
You are a TailwindCSS expert.

Constraints:
- At top: @tailwind base; @tailwind components; @tailwind utilities;
- Inside @layer base, define :root CSS variables for designSystem.colorPalette.
- Define font-family variables for designSystem.typography.
- Set scroll-behavior: smooth on html.
- Return only valid CSS, no comments or markdown.

Input:
{design_system}
'''
