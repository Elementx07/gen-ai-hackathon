import os

# prompts.py

# prompts.py

# Prompt to extract structured data from the user's description
DATA_EXTRACTION_PROMPT = """
You are a data analyst. A local artisan has provided a description of their business.
Your task is to extract structured data from this description and format it as a single JSON object.
The data should be comprehensive enough to build a full e-commerce website.

Business Description:
---
{description}
---

Based on the description, generate a JSON object with the following schema:
- "artisanInfo": An object containing:
  - "name": The artisan's or brand's name.
  - "story": A short, compelling story about the artisan.
  - "contact": An object with "email", "phone", and "address".
- "products": An array of product objects, each with:
  - "id": A unique integer ID.
  - "name": The product name.
  - "description": A brief description.
  - "price": A number (integer or float).
  - "imageUrl": A placeholder image URL from `https://placehold.co/600x400`.
- "galleryItems": An array of gallery objects, each with:
  - "id": A unique integer ID.
  - "name": A title for the gallery image.
  - "description": A brief description of the image.
  - "imageUrl": A placeholder image URL from `https://placehold.co/800x600`.
- "designSystem": An object containing:
  - "colorPalette": With "primary", "secondary", "accent", "text", and "background" hex codes.
  - "typography": With "headingFont" and "bodyFont" from Google Fonts.
  - "brandPersona": A few keywords describing the brand.

Return ONLY the raw JSON object.
"""

# Prompt to generate React components
REACT_COMPONENT_PROMPT = """
You are an expert React and Tailwind CSS developer.
Your task is to create a single, self-contained React component using Next.js, TypeScript, and Tailwind CSS.

JSON Data (includes design system and content):
---
{site_data}
---

Component to build: {component_name}
Component-specific data: {component_data}

Instructions:
1.  Use functional components with TypeScript.
2.  If the component uses React hooks (e.g., useState, useEffect), add "use client"; at the very top of the file.
3.  Use Tailwind CSS for all styling. Do NOT use CSS-in-JS, style tags, or separate CSS files. For interactive styles (like hover effects), use Tailwind's `hover:` utility classes (e.g., `hover:text-primary`, `hover:scale-105`) instead of inline `onMouseOver`/`onMouseOut` event handlers.
4.  Use the Next.js `<Image>` component for images and the `<Link>` component for navigation.
5.  The component should be fully responsive.
6.  The code should be clean, modern, and production-ready.
7.  Import `React` and other necessary hooks from 'react'.
8.  For props, define a `type` or `interface` for type safety. Ensure all necessary data from `site_data` (like `artisanInfo` and `designSystem`) is correctly defined in the props interface and utilized within the component.

Return ONLY the raw, complete `.tsx` code for the component. Do not include any explanations or markdown.
"""

# Prompt to generate Next.js pages
REACT_PAGE_PROMPT = """
You are an expert Next.js developer.
Your task is to create a page component for a Next.js 14+ application (using the App Router).

JSON Data (available in `@/data/products.json`):
---
{site_data}
---

Page to build: {page_name}

Instructions:
1.  The page should be a server-side component by default. Use `'use client';` only if client-side interactivity is essential (e.g., using React hooks).
2.  Import necessary components from the `@/components/` directory (e.g., `Navbar`, `Footer`, `ProductCard`). When importing and using components, ensure all their required props (e.g., `artisanInfo`, `designSystem`) are correctly passed.
3.  Use Tailwind CSS for styling.
4.  Fetch data directly from the `site_data` provided, as if you were importing it from `@/data/products.json`.
5.  Structure the page logically with `<main>`, `<section>`, etc.

Return ONLY the raw, complete `.tsx` code for the page. Do not include any explanations or markdown.
"""

# Prompt for the main layout file
LAYOUT_PROMPT = """
You are an expert Next.js developer creating the root layout for a new website.

JSON Data (available in `@/data/products.json`):
---
{site_data}
---

Instructions:
1.  Create a `RootLayout` component that wraps the `children`.
2.  Import the correct Google Fonts based on the `typography` section of the design system using `@next/font/google`.
3.  Import and use the `Navbar` and `Footer` components.
4.  Pass both `artisanInfo` and `designSystem` from the data as props to both the `Navbar` and `Footer` components.
5.  Set up the `metadata` object with the artisan's name and story for SEO.
6.  The file should include `import type {{ Metadata }} from "next";`.

Return ONLY the raw, complete `layout.tsx` code.
"""

# Prompt for the global CSS file
GLOBALS_CSS_PROMPT = """
You are a CSS specialist setting up the `globals.css` file for a new Next.js project using Tailwind CSS.

Design System:
---
{design_system}
---

Instructions:
1.  Include the three main Tailwind CSS directives: `@tailwind base;`, `@tailwind components;`, `@tailwind utilities;`.
2.  In the `@layer base`, define the color palette from the design system as CSS variables within the `:root` selector.
3.  Also in `@layer base`, set the `font-family` for `body` and `h1, h2, h3, h4, h5, h6` using the fonts from the design system, defining them as CSS variables first.
4.  Add a style for `scroll-behavior: smooth;` on the `html` element.

Return ONLY the raw, complete `globals.css` code.
"""


COMPONENT_PROMPT = """
You are an expert frontend developer. Your task is to create the HTML and CSS for a single, self-contained webpage component.
You must use the provided design system and component data.

Design System:
---
{design_system}
---

Component Data:
---
{component_data}
---

Component to build: {component_name}

Instructions:
1.  The HTML should be semantic and well-structured.
2.  The CSS must be fully responsive using media queries.
3.  Use the colors and fonts from the design system.
4.  The component should be visually appealing and modern.
5.  For image tags, use the provided image URLs. Do not use placeholders.

Return a single JSON object with two keys: "html" and "css".
The "css" should be the raw CSS content, not wrapped in <style> tags.
Return ONLY the raw JSON object.
"""

JAVASCRIPT_PROMPT = """
You are a senior JavaScript developer. Your task is to write a single, vanilla JavaScript script to add modern interactivity to a webpage.

The webpage has the following structure:
- A header with a navigation bar (`<nav>`). The nav has a button with the class `mobile-menu-button` and a menu with the class `mobile-menu`.
- Multiple sections (`<section>`) with the class `scroll-fade`.

Instructions:
1.  Write a script that toggles a 'hidden' class on the `mobile-menu` when the `mobile-menu-button` is clicked.
2.  Write a function that adds an 'is-visible' class to any element with the `scroll-fade` class when it scrolls into the viewport. This should create a fade-in effect.
3.  The script must have no external dependencies (vanilla JS only).
4.  The script should be efficient and well-commented.

Return ONLY the raw JavaScript code.
"""

ASSEMBLER_PROMPT = """
You are the lead developer assembling a webpage from components.
Your task is to create the final, single HTML file.

Design System:
---
{design_system}
---

HTML Components:
---
{html_components}
---

CSS Components:
---
{css_components}
---

JavaScript:
---
{javascript}
---

Instructions:
1.  Create a complete HTML5 document.
2.  In the `<head>`, import the specified Google Fonts.
3.  Combine all the CSS into a single `<style>` block in the `<head>`. Add a basic CSS reset at the top of the style block. Also add the CSS for the scroll-fade effect (`.scroll-fade {{ opacity: 0; transition: opacity 0.8s ease-in-out; }} .scroll-fade.is-visible {{ opacity: 1; }}`).
4.  In the `<body>`, assemble the HTML components in the correct order.
5.  At the end of the `<body>`, embed the provided JavaScript in a `<script>` block.

Return ONLY the final, raw HTML code.
"""
