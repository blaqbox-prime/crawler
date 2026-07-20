from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.Book import Book
from api.rate_limiter import limiter
from api.auth import generate_api_key, hash_api_key
from models.Api_Key import Api_key

router = APIRouter(prefix="/auth", tags=["auth"])
    
@router.post("/gen-key")
async def create_api_key(client_id: str):
    key = generate_api_key()
    api_key = Api_key(
        client_id=client_id,
        key_hash=hash_api_key(key)
    )
    
    existing_key = await Api_key.find_one(Api_key.client_id == client_id)
    if existing_key:
        existing_key.key_hash = api_key.key_hash
        await existing_key.save()
    else:
        await api_key.create()
    return {"api_key": key}
        
    

