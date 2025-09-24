# prompts.py

DATA_EXTRACTION_PROMPT = '''
You are a data analyst. 
A local artisan has provided a description of their business:
"{description}"

Extract structured data and return it as a single valid JSON object only.

Schema (required top-level keys):
-DO NOT ADD ''json fences at the start or end of the code.
- artisanInfo: object {{ name: string, story: string, contact: string (extract email/phone if mentioned, otherwise use "contact@[businessname].com" format) }}
- products: array of objects {{ id: string, name: string, description: string, price: string, imageUrl: string (use "/images/products/[product-name].jpg" format) }}
- galleryItems: array of objects {{ id: string, name: string, description: string, imageUrl: string (use "/images/gallery/[item-name].jpg" format) }}
- designSystem: object {{ colorPalette: object {{ primary: string, secondary: string, accent: string, background: string, text: string }}, typography: object {{ headingFont: string, bodyFont: string }}, brandPersona: string }}

Important:
- If contact info is not provided, generate a professional email using the business name
- For colorPalette, choose colors that match the artisan's style/products mentioned
- For typography, select Google Fonts that match the brand personality
- Generate 3-4 products minimum and 4-6 gallery items minimum
- All imageUrl paths should follow the specified format
'''


REACT_COMPONENT_PROMPT = '''
You are an expert React + TypeScript + Tailwind developer.

Constraints:
- Use Next.js App Router conventions.
- Always import `Link` from "next/link" if navigation is needed.
- Use dynamic routes correctly (e.g., /products/[id]).
- Use Next.js <Image> from "next/image".
- Define explicit prop types (interface).
- Only import from "next/*", "@/components", or "@/data".
- Import data from "@/data/products.json" when needed.
- Do not use external UI libraries (e.g., shadcn, MUI, Bootstrap).
- Code must be a single valid .tsx file.
- No markdown, no comments, no explanation outside the code.
- DO NOT ADD '' fences at the start or end of the code.

Input:
{site_data}
Component: {component_name}
Component data: {component_data}
'''



REACT_PAGE_PROMPT = '''
You are an expert Next.js developer.

Constraints:
- Generate a single .tsx file for a page in the App Router.
- Only import components that exist: ProductCard, Navbar, Footer, ContactForm
- Load site data only from "@/data/products.json".
- Use artisanInfo, products, galleryItems, and designSystem from the imported data.
- Do not use external libraries beyond Next.js, React, and Tailwind.
- Return only valid TypeScript/TSX code.
- No comments, no markdown, no extra text.
- DO NOT ADD '' fences at the start or end of the code.

Input:
{site_data}
Page: {page_name}
'''



LAYOUT_PROMPT = '''
You are an expert Next.js developer.

Constraints:
- Follow App Router layout conventions (layout.tsx).
- Import data from "@/data/products.json" and destructure artisanInfo and designSystem.
- Import Google Fonts using next/font/google based on designSystem.typography.headingFont and designSystem.typography.bodyFont.
- Import "@/components/Navbar" and "@/components/Footer".
- Pass artisanInfo and designSystem as props to these components.
- Set metadata.title = artisanInfo.name and metadata.description = artisanInfo.story.
- Export RootLayout.
- Return only valid TSX code, no comments or extra text.
- DO NOT ADD ''fences at the start or end of the code.

Input:
{site_data}
'''



GLOBALS_CSS_PROMPT = '''
You are a TailwindCSS expert.

Constraints:
- At top: @tailwind base; @tailwind components; @tailwind utilities;
- Inside @layer base, define :root CSS variables for designSystem.colorPalette (--color-primary, --color-secondary, etc.).
- Define font-family variables for designSystem.typography (--font-heading, --font-body).
- Set scroll-behavior: smooth on html.
- Use the color palette and typography from the provided design system.
- Return only valid CSS, no comments or markdown.
- DO NOT ADD fences '' at the start or end of the code.

Input:
{design_system}
'''
