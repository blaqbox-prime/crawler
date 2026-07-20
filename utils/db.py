from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import AsyncMongoClient
from beanie import init_beanie
from models.Book import Book
from models.Api_Key import Api_key


# MongoDB client setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncMongoClient("mongodb://localhost:27017")
    try:
        await init_beanie(database=client["filekeepers"], document_models=[Book, Api_key])
        yield
    except Exception as e:
        print(f"Error during database initialization: {e}")
    finally:
        await client.close()
        
async def fetchBooks():
    return await Book.find_all().to_list()
    