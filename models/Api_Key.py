from datetime import datetime
from pydantic import Field
from beanie import Document, Indexed


class Api_key(Document):
    client_id: Indexed(str, unique=True)
    is_active: bool = Field(default=True)
    create_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None
    key_hash: Indexed(str, unique=True)