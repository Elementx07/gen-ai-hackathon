import os
from typing import Optional, Type, TypeVar
from dotenv import load_dotenv
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
MODEL = os.environ.get("MODEL", "gemini-2.5-pro")

if not PROJECT_ID:
    raise ValueError("PROJECT_ID environment variable not set")
if not PROJECT_ID or PROJECT_ID == "YOUR_GOOGLE_CLOUD_PROJECT_ID":
    raise ValueError("PROJECT_ID not set. Set it in your .env file.")

# Initialize LangChain's VertexAI chat model
llm = ChatVertexAI(
    model=MODEL,
    project=PROJECT_ID,
    location=LOCATION,
    temperature=0.4,
    max_output_tokens=8024,
    max_retries=2,
)


def call_gemini(prompt: str, system_prompt: str = None, max_output_tokens: int = 8024, temperature: float = 0.4) -> str:
    """Legacy function for backward compatibility. Uses LangChain under the hood."""
    try:
        # Create a temporary LLM instance with specific parameters if different
        temp_llm = llm
        if temperature != 0.4 or max_output_tokens != 8024:
            temp_llm = ChatVertexAI(
                model=MODEL,
                project=PROJECT_ID,
                location=LOCATION,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                max_retries=2,
            )
        
        # Build messages
        messages = []
        if system_prompt:
            messages.append(("system", system_prompt))
        messages.append(("human", prompt))
        
        # Create chain
        prompt_template = ChatPromptTemplate.from_messages(messages)
        chain = prompt_template | temp_llm | StrOutputParser()
        
        # Execute with retry
        response = chain.invoke({})
        return response
    except Exception as e:
        logger.error(f"Error calling Gemini: {e}")
        raise


def call_gemini_structured(
    prompt: str,
    pydantic_model: Type[T],
    system_prompt: Optional[str] = None,
    temperature: float = 0.4,
    max_output_tokens: int = 8024,
) -> T:
    """
    Call Gemini with structured output using Pydantic models.
    
    Args:
        prompt: The user prompt
        pydantic_model: Pydantic model class for output parsing
        system_prompt: Optional system prompt
        temperature: Temperature for generation
        max_output_tokens: Maximum output tokens
        
    Returns:
        Parsed and validated Pydantic model instance
    """
    try:
        # Create LLM instance
        structured_llm = ChatVertexAI(
            model=MODEL,
            project=PROJECT_ID,
            location=LOCATION,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            max_retries=2,
        )
        
        # Create parser
        parser = JsonOutputParser(pydantic_object=pydantic_model)
        
        # Build messages with format instructions
        messages = []
        if system_prompt:
            messages.append(("system", system_prompt))
        
        # Add format instructions to the prompt
        format_instructions = parser.get_format_instructions()
        enhanced_prompt = f"{prompt}\n\n{format_instructions}"
        messages.append(("human", enhanced_prompt))
        
        # Create chain
        prompt_template = ChatPromptTemplate.from_messages(messages)
        chain = prompt_template | structured_llm | parser
        
        # Execute
        result = chain.invoke({})
        
        # Validate with Pydantic
        return pydantic_model.model_validate(result)
    except Exception as e:
        logger.error(f"Error calling Gemini with structured output: {e}")
        raise


def create_chain(
    prompt_template: str,
    system_prompt: Optional[str] = None,
    output_parser: Optional[any] = None,
):
    """
    Create a reusable LangChain chain.
    
    Args:
        prompt_template: Template string for the prompt
        system_prompt: Optional system prompt
        output_parser: Optional output parser (defaults to StrOutputParser)
        
    Returns:
        LangChain runnable chain
    """
    messages = []
    if system_prompt:
        messages.append(("system", system_prompt))
    messages.append(("human", prompt_template))
    
    prompt = ChatPromptTemplate.from_messages(messages)
    parser = output_parser or StrOutputParser()
    
    chain = prompt | llm | parser
    return chain
