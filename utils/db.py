from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient
from beanie import init_beanie
from models.Book import Book


# MongoDB client setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncMongoClient("mongodb://localhost:27017")
    try:
        await init_beanie(database=client["filekeepers"], document_models=[Book])
        yield
    except Exception as e:
        print(f"Error during database initialization: {e}")
    finally:
        await client.close()
        
async def fetchBooks():
    return await Book.find_all().to_list()
    