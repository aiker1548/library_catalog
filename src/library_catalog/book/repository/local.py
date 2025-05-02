import json
import os

from src.library_catalog.book.repository.base import AsyncBookRepositoryBase
from src.library_catalog.config import config

class BookRepositoryLocalStorage(AsyncBookRepositoryBase):
    def __init__(self, filepath=config.path_json_data):
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)

    async def _save_books(self, books):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=4)

    async def _load_books(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
        