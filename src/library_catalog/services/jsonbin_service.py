from typing import Annotated

from fastapi import Depends

from src.library_catalog.services.client_base import BaseApiClient

class JsonBinApiClient(BaseApiClient):
    def __init__(self, api_url='https://api.jsonbin.io/v3/b', api_key='your-api-key', id_collection='your-collection-id'):
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
        response = await self.client.put(f"{self.base_url}/{self.id_collection}", headers=self.build_headers(), json=data)
        response.raise_for_status()
        return response.json()

async def save_books_to_jsonbin(books: list):
    client = JsonBinApiClient(
        api_url='https://api.jsonbin.io/v3/b',
        api_key='$2a$10$p3QYbEprjYCrtersrsh9AeeCcoGqANmV94.mjUGGf74xfgtNJ7KCW',
        id_collection='6813c7c88561e97a500bbbb7'
    )
    try:
        response = await client.save_data(books)
        return response
    except Exception as e:
        raise Exception(f"Error saving data to JsonBin: {e}")
