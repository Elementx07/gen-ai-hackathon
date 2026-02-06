# Quick Start Guide: LangChain Integration

## What Changed?

This project now uses **LangChain** for AI orchestration, making it more reliable, maintainable, and extensible.

## Key Benefits

### 1. ✅ Type-Safe Data Validation
- **Before**: Manual JSON parsing with regex, prone to errors
- **After**: Pydantic models automatically validate all data

### 2. ✅ Better Error Handling  
- **Before**: Single retry, no backoff
- **After**: Built-in retry logic with proper error propagation

### 3. ✅ Maintainable Prompts
- **Before**: Long strings scattered in code
- **After**: Centralized prompt templates in `src/langchain_prompts.py`

### 4. ✅ Composable Chains
- **Before**: Repeated code for each generation task
- **After**: Reusable chains for components, pages, layouts

### 5. ✅ Production Ready
- **Before**: Basic error handling
- **After**: Enterprise-grade AI orchestration

## Files Added

```
src/
├── models.py              # Pydantic data models
├── ai_utils.py            # Enhanced with LangChain
├── langchain_prompts.py   # Prompt templates
└── website_generator.py   # Updated to use chains

test_langchain.py          # Test suite
README.md                  # Full documentation
LANGCHAIN_IMPROVEMENTS.md  # Detailed improvements
.gitignore                 # Clean repository
```

## Running the Application

### Prerequisites
```bash
pip install -r requirements.txt
export PROJECT_ID="your-google-cloud-project-id"
```

### Start the Application
```bash
streamlit run main.py
```

### Run Tests
```bash
python test_langchain.py
```

## Usage Example

The application now handles data extraction more reliably:

```python
# Old way (manual parsing)
response = call_gemini(prompt)
data = json.loads(regex_extract(response))  # May fail!

# New way (validated)
from src.models import SiteData
data = call_gemini_structured(
    prompt=prompt,
    pydantic_model=SiteData  # Auto-validated!
)
```

## What to Try

1. **Describe your artisan business** in natural language
2. **Click "Generate Website"** - watch the progress bar
3. **Download the generated website** as a ZIP file
4. **Extract and run**: `cd generated_website && npm install && npm run dev`

## Error Handling

LangChain now handles common issues automatically:
- ✅ Retries failed AI calls (up to 2 times)
- ✅ Validates output against Pydantic models
- ✅ Provides clear error messages
- ✅ Logs all operations for debugging

## Next Steps

With LangChain integrated, you can now:
- Add memory to remember user preferences
- Implement agents for multi-step reasoning
- Use RAG to incorporate best practices
- Stream responses in real-time
- Support multiple AI models with fallback

## Need Help?

- See `README.md` for full documentation
- See `LANGCHAIN_IMPROVEMENTS.md` for technical details
- Run `python test_langchain.py` to verify installation

## Architecture Diagram

```
User Input (Streamlit)
        ↓
[LangChain Orchestration Layer]
        ↓
   Pydantic Models (Validation)
        ↓
   Prompt Templates
        ↓
   Gemini AI (VertexAI)
        ↓
   JSON Output Parser
        ↓
   Validated Data
        ↓
Website Generation (Next.js)
```

## Before vs After Comparison

### Data Extraction
| Aspect | Before | After |
|--------|--------|-------|
| Parsing | Regex | JsonOutputParser |
| Validation | Manual | Pydantic automatic |
| Error handling | Try/catch | Built-in retry |
| Type safety | None | Full type safety |

### Code Generation
| Aspect | Before | After |
|--------|--------|-------|
| Prompts | String formatting | PromptTemplate |
| Reusability | Copy-paste | Chains |
| Testing | Hard | Easy (mock inputs) |
| Maintainability | Low | High |

## Success Indicators

You'll know LangChain is working when you see:
1. ✅ All tests pass: `python test_langchain.py`
2. ✅ Structured data extraction with validation
3. ✅ Automatic retries on failures
4. ✅ Clean, maintainable code
5. ✅ Better error messages

Enjoy building with LangChain! 🎉
