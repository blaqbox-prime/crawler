# Crawler API

A FastAPI-based book crawler that scrapes book data from books.toscrape.com, stores the results in MongoDB through Beanie, and exposes a small API for searching and retrieving books.

## Requirements

- Python: 3.10+ (the workspace was checked with Python 3.14.5)
- Core dependencies:
  - fastapi 0.115.x
  - beanie 1.26.x
  - pydantic 2.7.x to 2.9.x
  - pydantic-settings 2.3.x to 2.4.x
  - pymongo 4.8.x
  - httpx 0.27.x
  - beautifulsoup4 4.12.x
  - lxml 5.2.x to 5.3.x
  - apscheduler 3.10.x
  - slowapi 0.1.1

## Setup instructions

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the sample environment file and update it with your local values:
   ```bash
   copy .env.example .env
   ```

4. Start the API server:
   ```bash
   uvicorn api.main:app --reload
   ```

5. Optional: run the scheduler or trigger the crawl endpoint:
   ```bash
   http://127.0.0.1:8000/crawl
   ```

## Example .env file

A sample environment file is included in [.env.example](.env.example). A typical configuration looks like this:

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=filekeepers
CRAWL_BASE_URL=https://books.toscrape.com
CRAWL_CONCURRENCY=10
CRAWL_MAX_RETRIES=3
CRAWL_RETRY_BACKOFF_SECONDS=2.0
CRAWL_REQUEST_TIMEOUT=15.0
RAW_HTML_DIR=./raw_html
LOGS_DIR=logs
API_KEYS=dev-key-123
RATE_LIMIT=100/hour
API_PAGE_SIZE_DEFAULT=20
API_PAGE_SIZE_MAX=100
SCHEDULE_CRON_HOUR=2
SCHEDULE_CRON_MINUTE=0
```

## Sample MongoDB document structure

Each scraped book is stored as a document similar to this:

```json
{
  "_id": "9780000000000",
  "title": "Sample Book",
  "description": "A short description of the book.",
  "category": "Fiction",
  "price_including_tax": 14.99,
  "price_excluding_tax": 12.99,
  "availability": "In stock (20 available)",
  "number_of_reviews": 12,
  "cover_image_url": "https://books.toscrape.com/media/cache/....jpg",
  "rating": 4,
  "metadata": {
    "crawl_timestamp": "2026-07-20T10:00:00Z",
    "status": "200",
    "source_url": "https://books.toscrape.com/catalogue/sample-book/index.html"
  }
}
```

## Notes

- The crawler uses the `crawl_base_url` setting as its starting point.
- The API uses API key authentication for protected endpoints.
- The scheduler can be configured through the cron-related environment values.
