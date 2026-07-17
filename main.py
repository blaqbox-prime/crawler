from fastapi import FastAPI

app = FastAPI()

users = [{"id": 1, "name": "John Doe"}, {"id": 2, "name": "Jane Smith"}]

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/user")
async def getUser(index: int):
    if 0 <= index < len(users):
        return users[index]
    return {"error": "User not found"}

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
async def get_book_by_id(book_id: int):
    # Implementation for fetching a book by its ID
    pass

@app.get("/changes")
async def get_changes():
    # Implementation for fetching changes
    pass