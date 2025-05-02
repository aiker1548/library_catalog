import httpx
from typing import Any, Dict, Optional

from src.library_catalog.services.client_base import BaseApiClient
from src.library_catalog.config import config  

class OpenLibraryClient(BaseApiClient):
    """
    Клиент для работы с Open Library API.
    """
    def __init__(self, base_url: str = config.open_library_api_url):
        super().__init__(base_url=base_url)

    def build_headers(self) -> dict:
        # Open Library API не требует специальных заголовков
        return {"Accept": "application/json"}

    async def get_book_info(self, title: str) -> Dict[str, Any]:
        """
        По названию книги возвращает словарь с полями:
        {
            "rating": float | None,
            "image": str | None,
            "description": str | None
        }
        """
        first = await self._search_first_doc(title)
        if not first:
            return {"rating": None, "image": None, "description": None}

        key = first.get("key")            # e.g. "/works/OL11326416W"
        cover_id = first.get("cover_i")  # e.g. 8745958

        description = await self._get_description(key) if key else None
        rating = await self._get_rating(key) if key else None
        image = self._get_image_url(cover_id) if cover_id else None

        return {"rating": rating, "image": image, "description": description}

    async def _search_first_doc(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Выполняет поиск по заголовку и возвращает первый документ из списка docs.
        """
        resp = await self.get("search.json", params={"title": title})
        data = resp.json()
        docs = data.get("docs") or []
        return docs[0] if docs else None

    async def _get_description(self, key: str) -> Optional[str]:
        """
        По ключу work key получает описание книги.
        """
        try:
            resp = await self.get(f"{key}.json")
            data = resp.json()
            desc = data.get("description")
            if isinstance(desc, dict):
                return desc.get("value")
            if isinstance(desc, str):
                return desc
        except httpx.HTTPStatusError:
            return None
        return None

    async def _get_rating(self, key: str) -> Optional[float]:
        """
        По ключу work key получает средний рейтинг книги.
        """
        try:
            resp = await self.get(f"{key}/ratings.json")
            data = resp.json()
            summary = data.get("summary") or {}
            return summary.get("average")
        except httpx.HTTPStatusError:
            return None

    def _get_image_url(self, cover_id: int) -> str:
        """
        Строит URL обложки по cover_i.
        """
        return f"https://covers.openlibrary.org/b/id/{cover_id}.jpg"



