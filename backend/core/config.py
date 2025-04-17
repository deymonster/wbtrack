from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"  # для локальной разработки используем localhost

    N8N_API_KEY: str = "your-generated-api-key" 
    class Config:
        env_file = ".env"
        extra = "allow"
        env_file_encoding = "utf-8"

settings = Settings()
