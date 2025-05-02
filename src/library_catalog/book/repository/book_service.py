from src.library_catalog.book.repository.local import BookRepositoryLocalStorage
from src.library_catalog.book.models import Book, BookResponse, BookInfo
from src.library_catalog.services.jsonbin_service import save_books_to_jsonbin


class BookService:
    def __init__(self, repo: BookRepositoryLocalStorage):
        self.repo = repo

    async def add_book(self, book: BookInfo):
        await self.repo.add(book)
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
    


