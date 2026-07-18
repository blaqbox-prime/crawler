from fastapi import FastAPI
from utils.crawler import BooksCrawler
from models.Book import Book
from utils.db import lifespan

crawler = BooksCrawler()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    books = crawler.crawl_books()
    await Book.insert_many(books["books"])  # Save the crawled books to the database 
    return {"message": "Welcome to the Books API", "books": books}

# Books
@app.get("/books")
async def get_books(
    category: str = None, 
    min_price: float = None, 
    max_price: float = None,
    rating: float = None,
    sort_by: str = None) -> None:
    # Implementation for fetching books based on filters
    pass

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: str):
    # Implementation for fetching a book by its ID
    pass

@app.get("/changes")
async def get_changes():
    # Implementation for fetching changes
    pass