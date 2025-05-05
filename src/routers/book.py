from fastapi import APIRouter, Depends, HTTPException

from src.crud.book_service import BookServiceConnection
from src.schemas.book import Book, BookResponse
from src.database import DbSession

book_router = APIRouter()

@book_router.get("/books", response_model=list[BookResponse])
async def get_books(book_service_con: BookServiceConnection, db: DbSession):
    books = await book_service_con.list_all_books(db)
    return books

@book_router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_service_con: BookServiceConnection, book_id: int, db: DbSession):
    book = await book_service_con.get_book(book_id, db)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@book_router.post("/books", response_model=dict)
async def add_book(book_service_con: BookServiceConnection, book: Book, db: DbSession):
    await book_service_con.add_book(book, db)
    return {"message": "Book added successfully"}

@book_router.patch("/books/{book_id}", response_model=dict)
async def update_book(book_service_con: BookServiceConnection, book_id: int, book: dict, db: DbSession):
    existing_book = await  book_service_con.get_book(book_id, db)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    await book_service_con.update_book(book_id, book, db)
    return {"message": "Book updated successfully"}

@book_router.delete("/books/{book_id}", response_model=dict)
async def delete_book(book_service_con: BookServiceConnection, book_id: int, db: DbSession):
    existing_book = await book_service_con.get_book(book_id, db)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    await book_service_con.delete_book(book_id, db)
    return {"message": "Book deleted successfully"}
