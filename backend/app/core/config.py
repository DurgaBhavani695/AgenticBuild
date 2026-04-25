from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    LLM_PROVIDER: str = "groq"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
