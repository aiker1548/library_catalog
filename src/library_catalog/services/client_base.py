from abc import ABC, abstractmethod
import httpx

class BaseApiClient(ABC):
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=self.timeout)

    @abstractmethod
    def build_headers(self) -> dict:
        """Построить заголовки запроса."""
        pass

    async def get(self, endpoint: str, params: dict = None) -> httpx.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = await self.client.get(url, headers=self.build_headers(), params=params)
        response.raise_for_status()
        return response

    async def post(self, endpoint: str, data: dict = None, json: dict = None) -> httpx.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = await self.client.post(url, headers=self.build_headers(), data=data, json=json)
        response.raise_for_status()
        return response

    async def put(self, endpoint: str, data: dict = None) -> httpx.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = await self.client.put(url, headers=self.build_headers(), data=data)
        response.raise_for_status()
        return response

    async def delete(self, endpoint: str) -> httpx.Response:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = await self.client.delete(url, headers=self.build_headers())
        response.raise_for_status()
        return response

    async def close(self):
        await self.client.aclose()