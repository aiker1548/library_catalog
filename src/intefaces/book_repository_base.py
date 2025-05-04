from abc import ABC, abstractmethod
from typing import List

from src.schemas.book import Book, BookResponse

class AsyncBookRepositoryBase(ABC):
    @abstractmethod
    async def add(self, book: Book) -> BookResponse:
        """Добавление новой книги"""
        pass

    @abstractmethod
    async def update(self, book_id: int, book: dict) -> BookResponse:
        """Обновление данных книги"""
        pass

    @abstractmethod
    async def get_book(self, book_id: int) -> BookResponse:
        """Получение книги по ID"""
        pass

    @abstractmethod
    async def delete(self, book_id: int) -> None:
        """Удаление книги"""
        pass

    @abstractmethod
    async def list_all(self) -> List[BookResponse]:
        """Получение списка всех книг"""
        pass
