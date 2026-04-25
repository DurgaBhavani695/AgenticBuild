from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    LLM_PROVIDER: str = "groq"
    
    # Groq Settings (Default)
    GROQ_API_KEY: str = ""
    GROQ_MODEL_NAME: str = "openai/gpt-oss-120b"
    
    # OpenAI Settings (Optional fallback)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL_NAME: str = "gpt-4o"
    OPENAI_API_BASE: Optional[str] = None
    
    SECRET_KEY: str = "fallback-secret-key-change-this"
    DATABASE_URL: str = "sqlite:///./database.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
