import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    path_json_data: str = os.path.join("data", "books.json")  # Путь к файлу с данными книг
    jsonbin_api_url: str = "https://api.jsonbin.io/v3/b"  # URL API JsonBin
    jsonbin_api_key: str = os.getenv("JSONBIN_API_KEY", "your-api-key")  # API ключ JsonBin
    jsonbin_id_collection: str = os.getenv("JSONBIN_ID_COLLECTION", "your-collection-id")  # ID коллекции JsonBin
    open_library_api_url: str = "https://openlibrary.org"  # URL API OpenLibrary
    class Config:
        env_file = ".env"  # Путь к файлу .env


# Загружаем конфигурацию
config = Settings()