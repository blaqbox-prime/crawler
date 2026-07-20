from fastapi import FastAPI
from utils.crawler import BooksCrawler
from models.Book import Book
from utils.db import lifespan, fetchBooks
from api.routers import books

crawler = BooksCrawler()

app = FastAPI(lifespan=lifespan,
              title="FK Book Crawling API",
              description="Serves book data crawled from books.toscrape.com, with change history.",
              version="1.0.0",
              )

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Books API!"}

# Books
app.include_router(books.router)


@app.get("/changes")
async def get_changes():
    # Implementation for fetching changes
    pass


@app.get("/crawl")
async def get_crawl(page:int = 1):
    # Implementation for fetching crawled data
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