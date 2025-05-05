from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from loguru import logger

from src.schemas.book import Book, BookResponse
from src.models.book import Book as BookModel
from src.intefaces.book_repository_base import AsyncBookRepositoryBase


class SQLBookRepository(AsyncBookRepositoryBase):
    async def add(self, db: AsyncSession, book: Book):
        logger.info(f"Adding new book: {book.title}")
        db_book = BookModel(**book.model_dump(exclude_unset=True))
        db.add(db_book)
        try:
            await db.commit()
            await db.refresh(db_book)
            logger.success(f"Book added successfully: {db_book.id}")
            return db_book
        except SQLAlchemyError as e:
            await db.rollback()
            logger.exception(f"Failed to add book: {book.title}")
            raise

    async def update(self, db: AsyncSession, book_id: int, book_data: dict):
        logger.info(f"Updating book with ID: {book_id}")
        result = await db.execute(select(BookModel).where(BookModel.id == book_id))
        db_book = result.scalars().first()

        if not db_book:
            logger.warning(f"Book with ID {book_id} not found")
            raise HTTPException(status_code=404, detail="Book not found")

        for key, value in book_data.items():
            if hasattr(db_book, key) and value is not None:
                logger.debug(f"Updating field {key} to {value}")
                setattr(db_book, key, value)

        try:
            await db.commit()
            await db.refresh(db_book)
            logger.success(f"Book updated successfully: {book_id}")
            return db_book
        except SQLAlchemyError as e:
            await db.rollback()
            logger.exception(f"Failed to update book: {book_id}")
            raise

    async def get_book(self, db: AsyncSession, book_id: int):
        logger.info(f"Fetching book with ID: {book_id}")
        result = await db.execute(select(BookModel).where(BookModel.id == book_id))
        db_book = result.scalars().first()

        if not db_book:
            logger.warning(f"Book with ID {book_id} not found")
            raise HTTPException(status_code=404, detail="Book not found")

        logger.debug(f"Book retrieved: {db_book.title}")
        return BookResponse.model_validate(db_book)

    async def delete(self, db: AsyncSession, book_id: int):
        logger.info(f"Deleting book with ID: {book_id}")
        result = await db.execute(select(BookModel).where(BookModel.id == book_id))
        db_book = result.scalars().first()

        if not db_book:
            logger.warning(f"Book with ID {book_id} not found")
            raise HTTPException(status_code=404, detail="Book not found")

        await db.delete(db_book)
        try:
            await db.commit()
            logger.success(f"Book deleted successfully: {book_id}")
        except SQLAlchemyError as e:
            await db.rollback()
            logger.exception(f"Failed to delete book: {book_id}")
            raise

    async def list_all(self, db: AsyncSession):
        logger.info("Fetching all books")
        result = await db.execute(select(BookModel))
        books = result.scalars().all()
        logger.debug(f"Retrieved {len(books)} books")
        return [BookResponse.model_validate(b) for b in books]