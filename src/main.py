from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.book import book_router
from src.midlewares import DBSessionMiddleware

app = FastAPI(title="Library Catalog API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(DBSessionMiddleware)

app.include_router(book_router, tags=["books"])

