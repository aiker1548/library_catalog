import json
import os

from loguru import logger
from fastapi import HTTPException, status

from src.schemas.book import Book, BookResponse
from src.config import config
from src.intefaces.book_repository_base import AsyncBookRepositoryBase

class JsonBookRepository(AsyncBookRepositoryBase):
    def __init__(self, filepath=config.path_json_data):
        self.filepath = filepath
        logger.info(f"JsonBookRepository initialized with filepath: {filepath}")
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            logger.debug(f"Creating new JSON file at: {self.filepath}")
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)
            logger.success(f"JSON file created successfully at: {self.filepath}")

    async def _save_books(self, books):
        logger.debug(f"Saving {len(books)} books to: {self.filepath}")
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(books, f, ensure_ascii=False, indent=4)
            logger.success(f"Books saved successfully to: {self.filepath}")
        except Exception as e:
            logger.exception(f"Failed to save books to: {self.filepath}")
            raise

    async def _load_books(self):
        logger.debug(f"Loading books from: {self.filepath}")
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                books = json.load(f)
            logger.debug(f"Loaded {len(books)} books from: {self.filepath}")
            return books
        except FileNotFoundError:
            logger.warning(f"File not found: {self.filepath}, returning empty list")
            return []
        except Exception as e:
            logger.exception(f"Failed to load books from: {self.filepath}")
            raise

    async def add(self, book: Book):
        logger.info(f"Adding new book: {book.title}")
        try:
            books = await self._load_books()
        except FileNotFoundError:
            logger.warning(f"File not found, initializing empty book list")
            books = []

        if books:
            max_id = max(b["id"] for b in books)
            book_id = max_id + 1
        else:
            book_id = 1
        json_book = book.model_dump()
        json_book["id"] = book_id
        books.append(json_book)
        await self._save_books(books)
        logger.success(f"Book added successfully with ID: {book_id}")

    async def update(self, book_id: int, book: dict):
        logger.info(f"Updating book with ID: {book_id}")
        books = await self._load_books()
        for i, b in enumerate(books):
            if b['id'] == book_id:
                for key, value in book.items():
                    if value is not None:
                        logger.debug(f"Updating field {key} to {value}")
                        books[i][key] = value
                await self._save_books(books)
                logger.success(f"Book updated successfully: {book_id}")
                return
        logger.warning(f"Book with ID {book_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    async def get_book(self, book_id: int):   
        logger.info(f"Fetching book with ID: {book_id}")
        books = await self._load_books()
        for b in books:
            if b['id'] == book_id:
                logger.debug(f"Book retrieved: {b['title']}")
                return BookResponse.model_validate(b)
        logger.warning(f"Book with ID {book_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    async def delete(self, book_id: int):
        logger.info(f"Deleting book with ID: {book_id}")
        books = await self._load_books()
        initial_len = len(books)
        books = [b for b in books if b['id'] != book_id]
        if len(books) == initial_len:
            logger.warning(f"Book with ID {book_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        await self._save_books(books)
        logger.success(f"Book deleted successfully: {book_id}")

    async def list_all(self):
        logger.info("Fetching all books")
        books = await self._load_books()
        logger.debug(f"Retrieved {len(books)} books")
        return [BookResponse.model_validate(b) for b in books]