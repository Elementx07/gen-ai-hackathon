# prompts.py

DATA_EXTRACTION_PROMPT = '''
You are a data analyst. 
A local artisan has provided a description of their business:
"{description}"

Extract structured data and return it as a single valid JSON object only.

Schema (required top-level keys):
-DO NOT ADD ''json fences at the start or end of the code.
- artisanInfo: object {{ name: string, story: string, contact: string (extract email/phone if mentioned, otherwise use "contact@[businessname].com" format), address: string (if mentioned, otherwise generate realistic address), phone: string (if mentioned, otherwise generate format like "+1-XXX-XXX-XXXX") }}
- products: array of objects {{ id: string, name: string, description: string, price: string, category: string, imageUrl: string (use "/images/products/[product-name].jpg" format) }}
- galleryItems: array of objects {{ id: string, name: string, description: string, imageUrl: string (use "/images/gallery/[item-name].jpg" format) }}
- navigation: object {{ menuItems: array of objects {{ name: string, href: string, description: string }}, socialLinks: object {{ facebook: string (if mentioned), instagram: string (if mentioned), twitter: string (if mentioned), website: string (if mentioned) }} }}
- designSystem: object {{ colorPalette: object {{ primary: string, secondary: string, accent: string, background: string, text: string, muted: string }}, typography: object {{ headingFont: string, bodyFont: string, sizes: object {{ h1: string, h2: string, h3: string, body: string }} }}, brandPersona: string, logo: object {{ text: string, tagline: string }} }}
- siteSettings: object {{ title: string, description: string, keywords: array of strings, favicon: string, ogImage: string }}

Important:
- If contact info is not provided, generate professional contact details using the business name
- For navigation.menuItems, include: Home (/), Products (/products), Gallery (/gallery), About (/about), Contact (/contact)
- For colorPalette, choose colors that match the artisan's style/products mentioned
- For typography, select Google Fonts that match the brand personality
- Generate 4-6 products minimum and 6-8 gallery items minimum
- All imageUrl paths should follow the specified format
- Include realistic social media handles based on business name
- Generate SEO-friendly keywords related to the business
'''

NAVBAR_COMPONENT_PROMPT = '''
You are an expert React + TypeScript + Tailwind developer.

Create a responsive Navbar component that:
- Takes artisanInfo, navigation, and designSystem as props
- Uses navigation.menuItems for menu links
- Displays artisanInfo.name as logo/brand
- Uses designSystem.colorPalette for styling
- Uses designSystem.typography.headingFont for brand text
- Includes mobile hamburger menu
- Uses Next.js Link component for navigation
- Has proper TypeScript interfaces
- Is fully responsive

Constraints:
- Import Link from "next/link"
- Use only Tailwind CSS for styling
- No external UI libraries
- Return only valid TSX code
- No comments, no markdown
- DO NOT ADD ``` fences at the start or end

Input:
{site_data}
'''

FOOTER_COMPONENT_PROMPT = '''
You are an expert React + TypeScript + Tailwind developer.

Create a Footer component that:
- Takes artisanInfo, navigation, and designSystem as props
- Displays business name, contact info, and address
- Shows social media links from navigation.socialLinks
- Uses navigation.menuItems for footer links
- Uses designSystem.colorPalette for styling
- Uses designSystem.typography for fonts
- Includes copyright notice with current year
- Has multiple columns layout on desktop

Constraints:
- Import Link from "next/link"
- Use only Tailwind CSS for styling
- No external UI libraries
- Return only valid TSX code
- No comments, no markdown
- DO NOT ADD ``` fences at the start or end

Input:
{site_data}
'''

REACT_COMPONENT_PROMPT = '''
You are an expert React + TypeScript + Tailwind developer.

Create a {component_name} component that:
- Uses data from the provided site data
- Takes appropriate props (artisanInfo, products, galleryItems, designSystem, navigation as needed)
- Uses designSystem.colorPalette for all colors
- Uses designSystem.typography for fonts
- Is fully responsive
- Has proper TypeScript interfaces
- Uses Next.js conventions (Link, Image)

Constraints:
- Use Next.js App Router conventions
- Always import Link from "next/link" for navigation
- Use Next.js <Image> from "next/image" for images
- Define explicit prop types (interface)
- Only import from "next/*", "@/components", or "@/data"
- Import data from "@/data/products.json" when needed
- Do not use external UI libraries
- Code must be a single valid .tsx file
- No markdown, no comments
- DO NOT ADD ``` fences at the start or end

Input:
{site_data}
Component: {component_name}
Component data: {component_data}
'''

REACT_PAGE_PROMPT = '''
You are an expert Next.js developer.

Create a {page_name} page that:
- Loads site data from "@/data/products.json"
- Uses artisanInfo, products, galleryItems, designSystem, and navigation from imported data
- Uses designSystem.colorPalette for styling
- Uses designSystem.typography for fonts
- Uses navigation.menuItems for any internal links
- Is fully responsive and accessible
- Has proper SEO metadata

Constraints:
- Generate a single .tsx file for a page in the App Router
- Only import components that exist: ProductCard, Navbar, Footer, ContactForm, Hero
- Load site data only from "@/data/products.json"
- Do not use external libraries beyond Next.js, React, and Tailwind
- Return only valid TypeScript/TSX code
- No comments, no markdown
- DO NOT ADD ``` fences at the start or end

Input:
{site_data}
Page: {page_name}
'''

LAYOUT_PROMPT = '''
You are an expert Next.js developer.

Create a layout.tsx file that:
- Imports data from "@/data/products.json"
- Destructures artisanInfo, designSystem, navigation, and siteSettings
- Uses siteSettings for metadata (title, description)
- Imports Google Fonts (use Playfair_Display and Montserrat as defaults)
- Uses STATIC font variable names: "--font-heading" and "--font-body" (NOT dynamic)
- Passes artisanInfo, designSystem, and navigation as props to Navbar and Footer

Constraints:
- Follow App Router layout conventions (layout.tsx)
- Import "@/components/Navbar" and "@/components/Footer"
- Font variable names must be static literals: "--font-heading" and "--font-body"
- Set metadata from siteSettings data
- Export RootLayout with proper typing
- Return only valid TSX code
- No comments or extra text
- DO NOT ADD ``` fences at the start or end

Input:
{site_data}
'''

GLOBALS_CSS_PROMPT = '''
You are a TailwindCSS expert.

Create a globals.css file that:
- Includes Tailwind directives at the top
- Defines CSS variables for designSystem.colorPalette in :root
- Defines font-family variables for designSystem.typography
- Sets up smooth scrolling
- Defines custom utility classes for the design system
- Uses the exact color values and typography from the design system

Constraints:
- Start with: @tailwind base; @tailwind components; @tailwind utilities;
- Define CSS variables like --color-primary, --color-secondary, etc.
- Define font variables like --font-heading, --font-body
- Return only valid CSS
- No comments or markdown
- DO NOT ADD ``` fences at the start or end

Input:
{design_system}
'''
