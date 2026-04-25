from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from ..core.config import settings

def get_llm():
    if settings.LLM_PROVIDER.lower() == "groq":
        # Many users use OpenAI-compatible endpoints on Groq
        # This factory supports both native Groq and OpenAI-compatible versions
        return ChatGroq(
            api_key=settings.GROQ_API_KEY, 
            model_name=settings.GROQ_MODEL_NAME,
            temperature=0,
            max_tokens=4096  # Ensure enough room for large HTML files
        )
    elif settings.LLM_PROVIDER.lower() == "openai":
        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL_NAME,
            base_url=settings.OPENAI_API_BASE,
            temperature=0,
            max_tokens=4096
        )
    
    raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
