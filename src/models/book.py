from typing import Optional

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, Text, Float


Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    publication_year: Mapped[int] = mapped_column(Integer)
    genre: Mapped[str] = mapped_column(String(100))
    page_count: Mapped[int] = mapped_column(Integer)
    availability: Mapped[bool] = mapped_column(Boolean, default=True)
    image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    