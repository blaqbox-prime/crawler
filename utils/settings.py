from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Mongo
    mongo_uri: str = Field(default="mongodb://localhost:27017")
    mongo_db_name: str = Field(default="filekeepers")

    # Crawler
    crawl_base_url: str = Field(default="https://books.toscrape.com")
    crawl_concurrency: int = Field(default=10)
    crawl_max_retries: int = Field(default=3)
    crawl_retry_backoff_seconds: float = Field(default=2.0)
    crawl_request_timeout: float = Field(default=15.0)
    raw_html_dir: str = Field(default="./raw_html")
    logs_dir: str = Field(default="logs")
    
    # API
    api_keys: str = Field(default="dev-key-123")
    rate_limit: str = Field(default="100/hour")
    api_page_size_default: int = Field(default=20)
    api_page_size_max: int = Field(default=100)

    
    @property
    def api_key_set(self) -> List[str]:
        return [k.strip() for k in self.api_keys.split(",") if k.strip()]


@lru_cache
def get_settings() -> Settings:
    """Settings are cached so the .env file is only parsed once per process."""
    return Settings()
