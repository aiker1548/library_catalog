from fastapi import APIRouter, Depends, HTTPException

from src.crud.book_service import BookServiceConnection
from src.schemas.book import Book, BookResponse, BookInfo
from src.integrations.open_library.open_library_client import OpenLibraryClient

book_router = APIRouter()

@book_router.get("/books", response_model=list[BookResponse])
async def get_books(book_service_con: BookServiceConnection):
    books = await book_service_con.list_all_books()
    return books

@book_router.get("/books/{book_id}", response_model=BookResponse)
async def get_book(book_service_con: BookServiceConnection, book_id: int):
    book = await book_service_con.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@book_router.post("/books", response_model=dict)
async def add_book(book_service_con: BookServiceConnection,
                    book: Book,
                    open_library_client: OpenLibraryClient = Depends(OpenLibraryClient)):
    info = await open_library_client.get_book_info(book.title)
    book_create = BookInfo(
            **book.model_dump(),
            image=info.get("image"),
            description=info.get("description"),
            rating=info.get("rating")
        )

    await book_service_con.add_book(book_create)
    await open_library_client.close()

    return {"message": "Book added successfully"}

@book_router.patch("/books/{book_id}", response_model=dict)
async def update_book(book_service_con: BookServiceConnection, book_id: int, book: dict):
    existing_book = await  book_service_con.get_book(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    await book_service_con.update_book(book_id, book)
    return {"message": "Book updated successfully"}

@book_router.delete("/books/{book_id}", response_model=dict)
async def delete_book(book_service_con: BookServiceConnection, book_id: int):
    existing_book = await book_service_con.get_book(book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    await book_service_con.delete_book(book_id)
    return {"message": "Book deleted successfully"}
