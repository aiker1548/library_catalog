from abc import ABC, abstractmethod
import time

import httpx

from src.logger import logger  # Импортируем логгер

class BaseApiClient(ABC):
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=self.timeout)

        # Логируем открытие клиента
        logger.info(f"Initialized API client with base URL: {self.base_url}, timeout: {self.timeout}s")

    @abstractmethod
    def build_headers(self) -> dict:
        pass

    async def _request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        start = time.monotonic()
        try:
            response = await self.client.request(method, url, headers=self.build_headers(), **kwargs)
            elapsed = time.monotonic() - start
            logger.info(f"{method.upper()} {url} {response.status_code} in {elapsed:.2f}s")
            response.raise_for_status()
            return response
        except Exception as e:
            logger.exception(f"Error during {method.upper()} {url}: {e}")
            raise

    async def get(self, endpoint: str, params: dict = None) -> httpx.Response:
        return await self._request("GET", endpoint, params=params)

    async def post(self, endpoint: str, data: dict = None, json: dict = None) -> httpx.Response:
        return await self._request("POST", endpoint, data=data, json=json)

    async def put(self, endpoint: str, data: dict = None, json: dict = None) -> httpx.Response:
        return await self._request("PUT", endpoint, data=data, json=json)
    
    async def delete(self, endpoint: str) -> httpx.Response:
        return await self._request("DELETE", endpoint)

    async def close(self):
        # Логируем закрытие клиента
        logger.info("Closing API client connection.")
        await self.client.aclose()
