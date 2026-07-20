import secrets
import hashlib
from fastapi.security import APIKeyHeader
from fastapi import Security, HTTPException, status
from models.Api_Key import Api_key
from datetime import date, datetime

def generate_api_key() -> str:
    return f"sk_live_{secrets.token_urlsafe(32)}"

def hash_api_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(key: str = Security(api_key_header)):
    if not key:
        raise HTTPException(status_code=401, detail="No API Key provided")
    
    key_hash = hash_api_key(key)
    db_key = await Api_key.find_one(Api_key.key_hash == key_hash)
    if not db_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid API Key provided")
    if not db_key.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This API Key has been deactivated")
    if db_key.expires_at and db_key.expires_at < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This API Key has expired")
    return db_key