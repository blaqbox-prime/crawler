from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, date
from beanie import Document, Indexed

class Book(Document):
    id: str | None = None 
    title: str
    description: str
    category: Indexed(str)
    prices: dict[str, float]
    availability: str
    number_of_reviews: Indexed(int) = Field(..., ge=0)
    cover_image_url: str | None = None
    rating: Indexed(float) = Field(..., ge=0, le=5)
    metadata: Metadata | None = None
    
    crawl_timestamp: datetime
    status: str
    source_url: str
    