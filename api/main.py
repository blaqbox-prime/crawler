from fastapi import FastAPI
from utils.crawler import BooksCrawler
from models.Book import Book
from utils.db import lifespan
from api.routers import books, auth
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from api.rate_limiter import limiter
from utils.settings import get_settings


app = FastAPI(lifespan=lifespan,title="FK Book Crawling API",description="Serves book data crawled from books.toscrape.com, with change history.",version="1.0.0")

#rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(books.router)
app.include_router(auth.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Books API!"}




@app.get("/changes")
async def get_changes():
    # Implementation for fetching changes
    pass


@app.get("/crawl")
async def get_crawl(page:int = 1):
    crawler = BooksCrawler()
    crawl_data = await crawler.crawl_books(page_number=page)
    books_to_save = crawl_data.get("books", [])

    if books_to_save:
        for book in books_to_save:
            await Book.save(book)

    stored_books = await Book.find_all().to_list()
    return {
        **crawl_data,
        "books": [book.model_dump() for book in stored_books]
    }