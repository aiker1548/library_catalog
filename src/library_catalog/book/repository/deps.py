from typing import Annotated

from fastapi import Depends

from src.library_catalog.book.repository.local import BookRepositoryLocalStorage
from src.library_catalog.book.repository.book_service import BookService


async def get_book_service() -> BookService:
    return BookService(BookRepositoryLocalStorage())



BookServiceConnection = Annotated[BookService, Depends(get_book_service)]