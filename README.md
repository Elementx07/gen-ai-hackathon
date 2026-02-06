# AI-Powered Artisan Website Generator

An intelligent website generator that creates custom, professional websites for artisan businesses using AI and LangChain.

## Overview

This project uses **LangChain** with Google's Gemini AI to automatically generate complete Next.js websites from simple business descriptions. LangChain provides robust AI orchestration, structured output parsing, and error handling.

## Key Features

### 🤖 LangChain Integration
- **Structured Output Parsing**: Uses Pydantic models for type-safe data validation
- **Prompt Templates**: Maintainable, reusable prompt templates with LangChain
- **Chain Orchestration**: Sequential AI calls with built-in retry logic
- **Error Handling**: Automatic retries with exponential backoff
- **Type Safety**: Full TypeScript-style validation for Python using Pydantic

### 🎨 Website Generation
- Automatic Next.js + React + TypeScript website creation
- Responsive design with Tailwind CSS
- Complete component library (Navbar, Footer, Product Cards, Contact Forms)
- SEO-optimized pages
- Custom design system based on business description

### 📊 Structured Data Extraction
- Pydantic models ensure data consistency
- Validates all required fields
- Generates professional defaults when information is missing
- Type-safe data flow throughout the application

## How LangChain Improves This Project

### 1. **Better Prompt Management**
Before LangChain:
```python
# String concatenation, hard to maintain
prompt = f"Generate a website for {business_name}..."
response = call_ai(prompt)
```

After LangChain:
```python
# Reusable prompt templates
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    input_variables=["business_name"],
    template="Generate a website for {business_name}..."
)
chain = template | llm | parser
result = chain.invoke({"business_name": business_name})
```

### 2. **Structured Output Parsing**
Before:
```python
# Manual JSON parsing with error-prone regex
response = call_ai(prompt)
cleaned = response.strip().removeprefix("```json")
data = json.loads(match.group(0))  # Hope it works!
```

After:
```python
# Type-safe parsing with Pydantic validation
from src.models import SiteData

site_data = call_gemini_structured(
    prompt=prompt,
    pydantic_model=SiteData,  # Automatically validated!
)
```

### 3. **Automatic Retry Logic**
LangChain provides built-in retry mechanisms:
```python
llm = ChatVertexAI(
    model=MODEL,
    max_retries=2,  # Automatic retries on failure
)
```

### 4. **Chain Composition**
Build complex AI workflows:
```python
# Reusable chains for different tasks
component_chain = template | llm | StrOutputParser()
page_chain = page_template | llm | StrOutputParser()

# Easy to test, maintain, and extend
result = component_chain.invoke({"component_name": "Navbar"})
```

### 5. **Better Error Handling**
LangChain catches and handles errors at multiple levels, making the application more robust.

## Architecture

```
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   LangChain     │◄─── Prompt Templates
│   Orchestrator  │◄─── Pydantic Models
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Gemini AI     │
│  (VertexAI)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Next.js Files  │
│   Generated     │
└─────────────────┘
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export PROJECT_ID="your-google-cloud-project-id"
export GOOGLE_CLOUD_LOCATION="us-central1"
export MODEL="gemini-2.5-pro"
```

3. Run the application:
```bash
streamlit run main.py
```

## Usage

1. **Describe Your Business**: Enter a description of your artisan business, products, and services
2. **Generate Website**: Click "Generate Website Files" to create your custom website
3. **Download & Deploy**: Download the generated files and deploy to your hosting provider

Example input:
```
I am a potter named Sarah. I make unique, handmade ceramic mugs and bowls.
My style is rustic and earthy. I have 5 types of mugs (forest green, ocean blue, 
desert sand) and 3 types of bowls (small, medium, large). Mugs are $25, bowls 
are $40. Contact me at sarah@pottery.com.
```

## Project Structure

```
.
├── main.py                      # Streamlit UI entry point
├── requirements.txt             # Dependencies including LangChain
├── src/
│   ├── ai_utils.py             # LangChain AI utilities
│   ├── models.py               # Pydantic data models
│   ├── langchain_prompts.py    # LangChain prompt templates
│   ├── website_generator.py    # Website generation logic
│   ├── prompts.py              # Legacy prompts (for compatibility)
│   └── preview_server.py       # Local preview server
└── generated_website/          # Output directory
    └── src/
        ├── app/                # Next.js pages
        ├── components/         # React components
        └── data/               # Generated JSON data
```

## Key Components

### Pydantic Models (`src/models.py`)
Type-safe data structures:
- `SiteData`: Complete website data
- `ArtisanInfo`: Business information
- `Product`: Product details
- `DesignSystem`: Colors, fonts, branding

### LangChain Chains (`src/ai_utils.py`)
- `call_gemini()`: Legacy function with LangChain backend
- `call_gemini_structured()`: Structured output with Pydantic
- `create_chain()`: Create reusable LangChain chains

### Prompt Templates (`src/langchain_prompts.py`)
- Data extraction prompts
- Component generation prompts
- Page generation prompts
- CSS generation prompts

## Benefits of LangChain Integration

1. **Type Safety**: Pydantic models ensure data consistency
2. **Maintainability**: Prompt templates are easier to update
3. **Reliability**: Built-in retry logic and error handling
4. **Testability**: Individual chains can be tested in isolation
5. **Extensibility**: Easy to add new AI-powered features
6. **Multi-Model Support**: Switch between AI models easily
7. **Production Ready**: Enterprise-grade error handling and logging

## Future Enhancements

With LangChain, we can easily add:
- **Memory**: Remember user preferences across sessions
- **Agents**: Multi-step reasoning for complex website features
- **RAG**: Incorporate best practices from existing websites
- **Multi-Modal**: Process images for design inspiration
- **Streaming**: Real-time token streaming for better UX

## License

MIT
