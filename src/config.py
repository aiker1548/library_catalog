import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    #json_local
    path_json_data: str = os.path.join("data", "books.json")  # Путь к файлу с данными книг
    
    #jsonbin
    jsonbin_api_url: str = "https://api.jsonbin.io/v3/b"  # URL API JsonBin
    jsonbin_api_key: str = os.getenv("JSONBIN_API_KEY", "your-api-key")  # API ключ JsonBin
    jsonbin_id_collection: str = os.getenv("JSONBIN_ID_COLLECTION", "your-collection-id")  # ID коллекции JsonBin
    
    #open library
    open_library_api_url: str = "https://openlibrary.org"  # URL API OpenLibrary
    
    #posrgres
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/dbname")
    DATABASE_ENGINE_POOL_SIZE: int = 10
    DATABASE_ENGINE_POOL_TIMEOUT: int = 30
    DATABASE_ENGINE_POOL_RECYCLE: int = 1800
    DATABASE_ENGINE_MAX_OVERFLOW: int = 20
    DATABASE_ENGINE_POOL_PING: bool = True
    DATABASE_URL_ALT: str = os.getenv("DATABASE_URL_ALT", "")

    class Config:
        env_file = ".env"  # Путь к файлу .env


# Загружаем конфигурацию
config = Settings()