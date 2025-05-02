from typing import Annotated

from fastapi import Depends

from src.library_catalog.book.repository.local import BookRepositoryLocalStorage


async def get_repository_local() -> BookRepositoryLocalStorage:
    return BookRepositoryLocalStorage()


RepoSession = Annotated[BookRepositoryLocalStorage, Depends(get_repository_local)]