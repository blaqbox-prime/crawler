from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, date
from beanie import Document, Indexed
import pymongo

class Book(Document):
    id: str
    title: str
    description: str
    category: Indexed(str)
    price_including_tax: float = Field(..., ge=0)
    price_excluding_tax: float = Field(..., ge=0)
    availability: str
    number_of_reviews: Indexed(int) = Field(..., ge=0)
    cover_image_url: str | None = None
    rating: Indexed(float) = Field(..., ge=0, le=5)
    metadata: Metadata | None = None
    
        
    
class Metadata(BaseModel):
    crawl_timestamp: datetime
    status: str
    source_url: str
    