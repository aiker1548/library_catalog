from typing import Annotated

from fastapi import Depends

from src.crud.json_repository import JsonBookRepository
from src.schemas.book import Book, BookResponse, BookInfo
from src.integrations.services.save_to_json_bin import save_books_to_jsonbin
from src.integrations.open_library.open_library_client import OpenLibraryClient


class BookService:
    def __init__(self, repo: JsonBookRepository):
        self.repo = repo

    async def add_book(self, book: Book):
        open_library_client = OpenLibraryClient()
        info = await open_library_client.get_book_info(book.title)
        book_create = BookInfo(
            **book.model_dump(),
            image=info.get("image"),
            description=info.get("description"),
            rating=info.get("rating")
        )
        await self.repo.add(book_create)
        await open_library_client.close()
        books = await self.repo.list_all()
        await save_books_to_jsonbin([b.model_dump() for b in books])

    async def update_book(self, book_id: int, book_data: dict):
        await self.repo.update(book_id, book_data)
        books = await self.repo.list_all()
        await save_books_to_jsonbin([b.model_dump() for b in books])

    async def get_book(self, book_id: int) -> BookResponse:
        return await self.repo.get_book(book_id)

    async def delete_book(self, book_id: int):
        await self.repo.delete(book_id)
        books = await self.repo.list_all()
        await save_books_to_jsonbin([b.model_dump() for b in books])

    async def list_all_books(self) -> list[BookResponse]:
        return await self.repo.list_all()
    

async def get_book_repo() -> BookService:
    return BookService(JsonBookRepository())


BookServiceConnection = Annotated[BookService, Depends(get_book_repo)]


