from typing import Any, Dict, Optional

import httpx
from loguru import logger

from src.intefaces.client_api_base import BaseApiClient
from src.config import config  

class OpenLibraryClient(BaseApiClient):
    """
    Клиент для работы с Open Library API.
    """
    def __init__(self, base_url: str = config.open_library_api_url):
        super().__init__(base_url=base_url)
        logger.info(f"OpenLibraryClient initialized with base URL: {base_url}")

    def build_headers(self) -> dict:
        # Open Library API не требует специальных заголовков
        headers = {"Accept": "application/json"}
        logger.debug(f"Built headers: {headers}")
        return headers

    async def get_book_info(self, title: str) -> Dict[str, Any]:
        """
        По названию книги возвращает словарь с полями:
        {
            "rating": float | None,
            "image": str | None,
            "description": str | None
        }
        """
        logger.info(f"Fetching book info for title: {title}")
        first = await self._search_first_doc(title)
        if not first:
            logger.warning(f"No book found for title: {title}")
            return {"rating": None, "image": None, "description": None}

        key = first.get("key")            # e.g. "/works/OL11326416W"
        cover_id = first.get("cover_i")  # e.g. 8745958
        logger.debug(f"Found book with key: {key}, cover_id: {cover_id}")

        description = await self._get_description(key) if key else None
        rating = await self._get_rating(key) if key else None
        image = self._get_image_url(cover_id) if cover_id else None

        result = {"rating": rating, "image": image, "description": description}
        logger.success(f"Book info retrieved successfully for title: {title}")
        logger.debug(f"Result: {result}")
        return result

    async def _search_first_doc(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Выполняет поиск по заголовку и возвращает первый документ из списка docs.
        """
        logger.info(f"Searching for first document with title: {title}")
        try:
            resp = await self.get("search.json", params={"title": title})
            logger.debug(f"Search response status: {resp.status_code}")
            data = resp.json()
            docs = data.get("docs") or []
            if docs:
                logger.debug(f"Found {len(docs)} documents, returning first")
                return docs[0]
            logger.warning("No documents found")
            return None
        except Exception as e:
            logger.exception(f"Failed to search for title: {title}")
            raise

    async def _get_description(self, key: str) -> Optional[str]:
        """
        По ключу work key получает описание книги.
        """
        logger.info(f"Fetching description for key: {key}")
        try:
            resp = await self.get(f"{key}.json")
            logger.debug(f"Description response status: {resp.status_code}")
            data = resp.json()
            desc = data.get("description")
            if isinstance(desc, dict):
                logger.debug("Description is a dictionary, extracting value")
                return desc.get("value")
            if isinstance(desc, str):
                logger.debug("Description is a string")
                return desc
            logger.warning("No description found")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while fetching description for key: {key}, status: {e.response.status_code}")
            return None
        except Exception as e:
            logger.exception(f"Failed to fetch description for key: {key}")
            raise

    async def _get_rating(self, key: str) -> Optional[float]:
        """
        По ключу work key получает средний рейтинг книги.
        """
        logger.info(f"Fetching rating for key: {key}")
        try:
            resp = await self.get(f"{key}/ratings.json")
            logger.debug(f"Rating response status: {resp.status_code}")
            data = resp.json()
            summary = data.get("summary") or {}
            rating = summary.get("average")
            logger.debug(f"Rating: {rating}")
            return rating
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while fetching rating for key: {key}, status: {e.response.status_code}")
            return None
        except Exception as e:
            logger.exception(f"Failed to fetch rating for key: {key}")
            raise

    def _get_image_url(self, cover_id: int) -> str:
        """
        Строит URL обложки по cover_i.
        """
        image_url = f"https://covers.openlibrary.org/b/id/{cover_id}.jpg"
        logger.debug(f"Built image URL: {image_url}")
        return image_url