from src.integrations.json_bin.json_bin_client import JsonBinApiClient
from src.config import config

async def save_books_to_jsonbin(books: list):
    """
    Функция для сохранения книг в удаленной коллекции
    """
    client = JsonBinApiClient(
        api_key=config.jsonbin_api_key,
        id_collection=config.jsonbin_id_collection,
    )
    try:
        response = await client.save_data(books)
        return response
    except Exception as e:
        raise Exception(f"Error saving data to JsonBin: {e}")
    finally:
        await client.close()