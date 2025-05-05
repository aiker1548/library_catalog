from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from src.schemas.book import Book, BookResponse
from src.models.book import Book as BookModel
from src.intefaces.book_repository_base import AsyncBookRepositoryBase


class SQLBookRepository(AsyncBookRepositoryBase):
    async def add(self, db: AsyncSession, book: Book):
        db_book = BookModel(**book.model_dump(exclude_unset=True))
        db.add(db_book)
        try:
            await db.commit()
            await db.refresh(db_book)
        except SQLAlchemyError:
            await db.rollback()
            raise
        return db_book

    async def update(self, db: AsyncSession, book_id: int, book_data: dict):
        result = await db.execute(select(BookModel).where(BookModel.id == book_id))
        db_book = result.scalars().first()

        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")

        for key, value in book_data.items():
            if hasattr(db_book, key) and value is not None:
                setattr(db_book, key, value)

        try:
            await db.commit()
            await db.refresh(db_book)
        except SQLAlchemyError:
            await db.rollback()
            raise

        return db_book

    async def get_book(self, db: AsyncSession, book_id: int):
        result = await db.execute(select(BookModel).where(BookModel.id == book_id))
        db_book = result.scalars().first()

        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")

        return BookResponse.model_validate(db_book)

    async def delete(self, db: AsyncSession, book_id: int):
        result = await db.execute(select(BookModel).where(BookModel.id == book_id))
        db_book = result.scalars().first()

        if not db_book:
            raise HTTPException(status_code=404, detail="Book not found")

        await db.delete(db_book)
        try:
            await db.commit()
        except SQLAlchemyError:
            await db.rollback()
            raise

    async def list_all(self, db: AsyncSession):
        result = await db.execute(select(BookModel))
        books = result.scalars().all()
        return [BookResponse.model_validate(b) for b in books]
