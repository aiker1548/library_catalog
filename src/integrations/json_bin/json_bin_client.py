from src.intefaces.client_api_base import BaseApiClient
from src.config import config

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