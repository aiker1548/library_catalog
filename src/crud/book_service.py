from typing import Annotated, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.json_repository import JsonBookRepository
from src.crud.sql_repository import SQLBookRepository 
from src.schemas.book import Book, BookResponse, BookInfo
from src.integrations.services.save_to_json_bin import save_books_to_jsonbin
from src.integrations.open_library.open_library_client import OpenLibraryClient


class BookService:
    def __init__(
        self,
        json_repo: JsonBookRepository,
        sql_repo: SQLBookRepository,
    ):
        self.json_repo = json_repo
        self.sql_repo = sql_repo

    async def add_book(self, book: Book, db: Optional[AsyncSession] = None) -> BookResponse:
        # Получаем доп. информацию из OpenLibrary
        open_library_client = OpenLibraryClient()
        info = await open_library_client.get_book_info(book.title)
        book_info = BookInfo(
            **book.model_dump(),
            image=info.get("image"),
            description=info.get("description"),
            rating=info.get("rating")
        )
        # Сохраняем в JSON
        await self.json_repo.add(book_info)
        # Сохраняем в SQL БД
        await self.sql_repo.add(db, book_info)
        # Закрываем клиент OpenLibrary
        await open_library_client.close()
        # Получаем актуальный список
        books = await self.json_repo.list_all()
        # Отправляем в JSONBin
        await save_books_to_jsonbin([b.model_dump() for b in books])

    async def update_book(self, book_id: int, book_data: dict, db: Optional[AsyncSession] = None):
        # Обновляем в JSON
        await self.json_repo.update(book_id, book_data)
        # Обновляем в SQL
        await self.sql_repo.update(db, book_id, book_data)
        # Сохраняем актуальный JSONBin
        books = await self.json_repo.list_all()
        await save_books_to_jsonbin([b.model_dump() for b in books])

    async def get_book(self, book_id: int, db: Optional[AsyncSession] = None) -> BookResponse:
        # Читаем из SQL для актуальности
        db_book = await self.sql_repo.get_book(db, book_id)
        return db_book

    async def delete_book(self, book_id: int, db: Optional[AsyncSession] = None):
        # Удаляем из JSON
        await self.json_repo.delete(book_id)
        # Удаляем из SQL
        await self.sql_repo.delete(db, book_id)
        # Обновляем JSONBin
        books = await self.json_repo.list_all()
        await save_books_to_jsonbin([b.model_dump() for b in books])

    async def list_all_books(self, db: Optional[AsyncSession] = None) -> list[BookResponse]:
        # Список из SQL
        books = await self.sql_repo.list_all(db)
        return books


async def get_book_service() -> BookService:
    json_repo = JsonBookRepository()
    sql_repo = SQLBookRepository()
    return BookService(json_repo=json_repo, sql_repo=sql_repo)


BookServiceConnection = Annotated[BookService, Depends(get_book_service)]
