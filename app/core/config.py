from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'Stylish AI'
    environment: str = 'development'
    secret_key: str = Field(default='change-me-in-production', min_length=16)
    access_token_expire_minutes: int = 60 * 24
    algorithm: str = 'HS256'

    database_url: str = 'sqlite+aiosqlite:///./stylish_ai.db'
    redis_url: str = 'redis://redis:6379/0'
    rapidapi_key: str = ''
    rapidapi_url: str = 'https://try-on-diffusion.p.rapidapi.com/try-on-file'
    rapidapi_host: str = 'try-on-diffusion.p.rapidapi.com'
    openai_api_key: str = ''
    use_ollama: bool = False
    ollama_model: str = 'llama3.1'

    max_upload_size: int = 4 * 1024 * 1024


@lru_cache
def get_settings() -> Settings:
    return Settings()
