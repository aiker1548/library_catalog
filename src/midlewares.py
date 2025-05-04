from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from src.database import AsyncSessionMaker

class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Генерация уникального ID запроса

        # Создаем сессию для этого запроса и прокидываем её в request.state.db
        async with AsyncSessionMaker() as session:
            request.state.db = session  # Прокидываем сессию
            response = await call_next(request)  # Обрабатываем запрос
            await session.close()  # Закрываем сессию после запроса

        return response