from typing import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.json_repository import JsonBookRepository
from src.crud.sql_repository import SQLBookRepository

def get_json_book_repo():
      return JsonBookRepository()

def get_sql_book_repo():
      return SQLBookRepository()

# Функция для получения сессии из request.state.db
async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии БД из request.state."""
    db_session = request.state.db  # Получаем сессию из request.state
    try:
        yield db_session  # Возвращаем сессию в качестве контекста
    except Exception:
        await db_session.rollback()  # Откат при ошибке
        raise
    finally:
        # Сессия будет закрыта в middleware после запроса
        pass