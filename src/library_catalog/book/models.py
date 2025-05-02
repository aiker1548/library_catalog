from pydantic import BaseModel, Field

class Book(BaseModel):
    title: str = Field(..., title="Book Title", description="Title of the book")
    author: str = Field(..., title="Author", description="Author of the book")
    publication_year: int = Field(..., title="Publication Year", description="Year the book was published")
    genre: str = Field(..., title="Genre", description="Genre of the book")
    page_count: int = Field(..., title="Page Count", description="Number of pages in the book")
    availability : bool = Field(..., title="Availability", description="Availability status of the book")

class BookResponse(Book):
    id: int = Field(..., title="Book ID", description="Unique identifier for the book")