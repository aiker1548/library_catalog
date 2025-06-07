from loguru import logger

from src.intefaces.client_api_base import BaseApiClient
from src.config import config

class JsonBinApiClient(BaseApiClient):
    def __init__(self, api_url=config.jsonbin_api_url, api_key='your-api-key', id_collection='your-collection-id'):
        super().__init__(base_url=api_url)
        self.api_key = api_key
        self.headers = {'X-Master-Key': api_key}
        self.id_collection = id_collection
        logger.info(f"JsonBinApiClient initialized with collection ID: {self.id_collection}")

    def build_headers(self) -> dict:
        headers = {
            'X-Master-Key': self.api_key,
            'Content-Type': 'application/json'
        }
        logger.debug(f"Built headers: {headers}")
        return headers

    async def save_data(self, data: dict) -> dict:
        """
        Сохраняет данные в удаленной коллекции и возвращает результат.
        """
        endpoint = str(self.id_collection)
        logger.info(f"Saving data to endpoint: {endpoint}")
        logger.debug(f"Payload: {data}")

        try:
            response = await self.put(endpoint, json=data)
            logger.debug(f"Response status: {response.status_code}")
            result = response.json()
            logger.success("Data saved successfully")
            return result
        except Exception as e:
            logger.exception("Failed to save data")
            raise
