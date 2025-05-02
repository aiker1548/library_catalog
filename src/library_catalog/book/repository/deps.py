from typing import Annotated

from fastapi import Depends

from src.library_catalog.book.repository.local import BookRepositoryLocalStorage
from src.library_catalog.book.repository.book_service import BookService


async def get_book_service() -> BookService:
    return BookService(RepoSession())

async def get_repository_local() -> BookRepositoryLocalStorage:
    return BookRepositoryLocalStorage()

BookServiceConnection = Annotated[BookService, Depends(get_book_service)]
RepoSession = Annotated[BookRepositoryLocalStorage, Depends(get_repository_local)]