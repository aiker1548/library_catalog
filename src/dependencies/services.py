from fastapi import Depends

from src.crud.json_repository import JsonBookRepository
from src.crud.sql_repository import SQLBookRepository
from src.crud.book_service import BookService
from src.dependencies.db import get_json_book_repo, get_sql_book_repo

def get_book_service(
        json_repo: JsonBookRepository = Depends(get_json_book_repo),
        sql_repo: SQLBookRepository = Depends(get_sql_book_repo)
):
    return BookService(json_repo, sql_repo)

