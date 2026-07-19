from fastapi import FastAPI
from utils.crawler import BooksCrawler
from models.Book import Book
from utils.db import lifespan, fetchBooks

crawler = BooksCrawler()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Books API!"}

# Books
@app.get("/books")
async def get_books(
    category: str = None, 
    min_price: float = None, 
    max_price: float = None,
    rating: float = None,
    sort_by: str = None) -> None:
    # Implementation for fetching books based on filters
    books = await Book.find_all().to_list()
    return {"Books": books}

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: str):
    # Implementation for fetching a book by its ID
    pass

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