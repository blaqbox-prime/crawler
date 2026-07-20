from contextlib import asynccontextmanager
from fastapi import FastAPI
from pymongo import AsyncMongoClient
from beanie import init_beanie
from models.Book import Book
from models.Api_Key import Api_key
from utils.settings import get_settings


# MongoDB client setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncMongoClient(get_settings().mongo_uri)
    try:
        await init_beanie(database=client[get_settings().mongo_db_name], document_models=[Book, Api_key])
        yield
    except Exception as e:
        print(f"Error during database initialization: {e}")
    finally:
        await client.close()
        