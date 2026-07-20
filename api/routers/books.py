from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from models.Book import Book
from api.rate_limiter import limiter



router = APIRouter(prefix="/books", tags=["books"])
# Sorting Options
SORT_FIELD_MAP = {
    "rating": "rating",
    "price": "price_including_tax",
    "reviews": "number_of_reviews",
}

@router.get("")
async def get_books(
    request: Request,
    category: Optional[str] = Query(default=None, description="Filter by exact category name"),
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    rating: Optional[int] = Query(default=None, ge=1, le=5),
    sort_by: Optional[str] = Query(default=None, description="rating | price | reviews"),
    order: str = Query(default="asc", pattern="^(asc|desc)$")):
    # Implementation for fetching books based on filters
    query: dict = {} #will hold filters if any are in the query params
    if category:
        query["category"] = category
    if rating:
        query["rating"] = rating
    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        query["price_including_tax"] = price_filter
    
    # return 403 Bad Request if sort is invalid
    if sort_by and sort_by not in SORT_FIELD_MAP:
        raise HTTPException(status_code=400, detail=f"sort_by must be one of {list(SORT_FIELD_MAP)}")    
    
    # fetch books
    count_of_books = await Book.count()
    books = await Book.find(query).to_list()
    
    # Sort the fetched books
    if sort_by:
        reverse = True if order == "desc" else False
        sort_field = SORT_FIELD_MAP[sort_by]
        try:
            books = sorted(books, key=lambda b: getattr(b, sort_field) if hasattr(b, sort_field) else (b.model_dump().get(sort_field) if hasattr(b, "model_dump") else None), reverse=reverse)
        except Exception:
            # fallback: return unsorted if something unexpected happens
            pass
    
    books_to_return = [b.model_dump() for b in books]
    
    return {"total": count_of_books,"count": len(books_to_return),"Books": books_to_return}


@router.get("/{book_id}")
async def get_book(
    request: Request,
    book_id: str,
):
    """`book_id` is the book's UPC (its natural unique key from the source site)."""
    book = await db.books.find_one({"_id": book_id})
    if not book:
        raise HTTPException(status_code=404, detail=f"No book found with id '{book_id}'")
    return book.model_dump_json()