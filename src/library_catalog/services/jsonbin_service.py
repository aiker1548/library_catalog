from src.library_catalog.services.client_base import BaseApiClient
from src.library_catalog.config import config

class JsonBinApiClient(BaseApiClient):
    def __init__(self, api_url=config.jsonbin_api_url, api_key='your-api-key', id_collection='your-collection-id'):
        super().__init__(base_url=api_url)
        self.api_key = api_key
        self.headers = {'X-Master-Key': api_key}
        self.id_collection = id_collection
    
    
    def build_headers(self) -> dict:
        return {
            'X-Master-Key': self.api_key,
            'Content-Type': 'application/json'
        }
    
    async def save_data(self, data: dict):
        """
        Сохраняет данные в удаленной коллекции
        """
        response = await self.client.put(f"{self.base_url}/{self.id_collection}", headers=self.build_headers(), json=data)
        response.raise_for_status()
        return response.json()

async def save_books_to_jsonbin(books: list):
    """
    Функция для сохранения книг в удаленной коллекции
    """
    client = JsonBinApiClient(
        api_key=config.jsonbin_api_key,
        id_collection=config.jsonbin_id_collection,
    )
    try:
        response = await client.save_data(books)
        return response
    except Exception as e:
        raise Exception(f"Error saving data to JsonBin: {e}")
    finally:
        await client.close()