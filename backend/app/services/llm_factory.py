from langchain_groq import ChatGroq
from ..core.config import settings

def get_llm():
    if settings.LLM_PROVIDER.lower() == "groq":
        return ChatGroq(api_key=settings.GROQ_API_KEY, model_name="llama3-8b-8192")
    # Add other providers here later
    raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
