from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient
from beanie import init_beanie
from models.Book import Book


# MongoDB client setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncMongoClient("mongodb://localhost:27017")
    await init_beanie(
        database=client["filekeepers"],
        document_models=[Book],
    )
    yield