from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from src.dependencies.services import get_book_service
from src.dependencies.db import get_async_session
from src.schemas.book import Book, BookResponse

book_router = APIRouter()


@book_router.get("/books", response_model=list[BookResponse])
async def get_books(book_service_con = Depends(get_book_service)):
    logger.info("GET /books — retrieving all books")
    books = await book_service_con.list_all_books()
    logger.debug(f"Found {len(books)} books")
    return books


@book_router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, book_service_con = Depends(get_book_service)):
    logger.info(f"GET /books/{book_id} — retrieving book")
    book = await book_service_con.get_book(book_id)
    if not book:
        logger.warning(f"Book with id {book_id} not found")
        raise HTTPException(status_code=404, detail="Book not found")
    logger.debug(f"Book found: {book}")
    return book


@book_router.post("/books", response_model=dict)
async def add_book(book: Book, book_service_con = Depends(get_book_service)):
    logger.info("POST /books — adding new book")
    logger.debug(f"Book data: {book}")
    await book_service_con.add_book(book)
    logger.success("Book added successfully")
    return {"message": "Book added successfully"}


@book_router.patch("/books/{book_id}", response_model=dict)
async def update_book(book_id: int, book: dict, book_service_con = Depends(get_book_service)):
    logger.info(f"PATCH /books/{book_id} — updating book")
    existing_book = await book_service_con.get_book(book_id)
    if not existing_book:
        logger.warning(f"Book with id {book_id} not found for update")
        raise HTTPException(status_code=404, detail="Book not found")
    
    logger.debug(f"Update data: {book}")
    await book_service_con.update_book(book_id, book)
    logger.success(f"Book with id {book_id} updated successfully")
    return {"message": "Book updated successfully"}


@book_router.delete("/books/{book_id}", response_model=dict)
async def delete_book(book_id: int,book_service_con = Depends(get_book_service)):
    logger.info(f"DELETE /books/{book_id} — deleting book")
    existing_book = await book_service_con.get_book(book_id)
    if not existing_book:
        logger.warning(f"Book with id {book_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Book not found")
    
    await book_service_con.delete_book(book_id)
    logger.success(f"Book with id {book_id} deleted successfully")
    return {"message": "Book deleted successfully"}
