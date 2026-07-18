from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, date


class Book(BaseModel):
    id: str = str(uuid4())
    title: str
    description: str
    category: str
    prices: dict[str, float]
    availability: bool
    number_of_reviews: int = Field(..., ge=0)
    cover_image_url: HttpUrl | None = None
    rating: float = Field(..., ge=0, le=5)
    metadata: Metadata | None = None
    
class Metadata(BaseModel):
    crawl_timestamp: datetime
    status: str
    source_url: str
    