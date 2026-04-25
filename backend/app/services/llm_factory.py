from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from ..core.config import settings

def get_llm(model_name: str = None):
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "groq":
        active_model = model_name or settings.GROQ_MODEL_NAME
        return ChatGroq(
            api_key=settings.GROQ_API_KEY, 
            model_name=active_model,
            temperature=0,
            max_tokens=8192
        )
    elif provider == "openai":
        active_model = model_name or settings.OPENAI_MODEL_NAME
        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=active_model,
            base_url=settings.OPENAI_API_BASE,
            temperature=0,
            max_tokens=8192
        )
    
    raise ValueError(f"Unsupported LLM provider: {provider}")
