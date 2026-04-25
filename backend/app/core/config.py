from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    LLM_PROVIDER: str = "groq"
    GROQ_MODEL_NAME: str = "llama3-8b-8192"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
