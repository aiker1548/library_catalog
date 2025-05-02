from fastapi import HTTPException, status

from src.library_catalog.book.models import Book, BookResponse

class AsyncBookRepositoryBase:
    async def add(self, book: Book):
        try:
            books = await self._load_books()
        except FileNotFoundError:
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
    
    async def update(self, book_id: int, book: dict):
        books = await self._load_books()
        for i, b in enumerate(books):
            if b['id'] == book_id:
                for key, value in book.items():
                    if value is not None:  
                        books[i][key] = value
                break
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        await self._save_books(books)

    async def get_book(self, book_id: int):   
        books = await self._load_books()
        for b in books:
            if b['id'] == book_id:
                return BookResponse.model_validate(b)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    async def delete(self, book_id: int):
        books = await self._load_books()
        books = [b for b in books if b['id'] != book_id]
        await self._save_books(books)

    async def list_all(self):
        books = await self._load_books()
        return [BookResponse.model_validate(b) for b in books]