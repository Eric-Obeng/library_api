from fastapi import FastAPI, HTTPException
from constant.book import Books
from model.book import Book, CreateBook

app = FastAPI()

books = Books


# A. Root Endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Library API!"}


# B. Get Book by ID
@app.get("/books/{book_id}")
def get_book_by_id(book_id: int) -> Book:
    if book_id < 0:
        raise HTTPException(status_code=400, detail="Invalid book ID.")

    for book in books:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found.")


# C. Search for Books
@app.get("/search")
def search_books(title: str = None, author: str = None, limit: int = 5) -> dict:
    search_results = books

    if title:
        search_results = [
            book for book in search_results if title.lower() in book.title.lower()
        ]

    if author:
        search_results = [
            book for book in search_results if author.lower() in book.author.lower()
        ]

    search_results = search_results[:limit]

    if not search_results:
        raise HTTPException(status_code=400, detail="No books found.")

    return {"results": search_results, "count": len(search_results)}


# D. Filter Books by Category
@app.get("/category/{category_name}")
def filter_book_by_category(category_name: str, sort: str = None) -> dict:
    filtered_book = [
        book for book in books if book.category.lower() == category_name.lower()
    ]

    if sort:
        sort_lower = sort.lower()
        if sort_lower not in ("asc", "desc"):
            raise HTTPException(
                status_code=400, detail="Invalid sort value. User 'asc' or 'desc'."
            )
        reverse = sort_lower == "desc"
        filtered_book.sort(key=lambda b: b.title.lower(), reverse=reverse)

    if not filtered_book:
        raise HTTPException(status_code=400, detail="No books found.")

    return {"result": filtered_book, "count": len(filtered_book)}


@app.post("/book", response_model=Book, status_code=201)
def create_book(payload: CreateBook):
    _id = len(books) + 1

    new_book = Book(
        id=_id,
        title=payload.title,
        author=payload.author,
        category=payload.category,
        description=payload.description,
    )
    books.append(new_book)

    return new_book


@app.put("/books/{book_id}")
def update_book(book_id: int, payload: CreateBook) -> Book:
    if book_id < 0 or book_id > len(books):
        raise HTTPException(status_code=400, detail="Invalid book ID.")

    index = book_id - 1

    book = books[index]
    updated_book = payload.model_dump()

    for field, value in updated_book.items():
        setattr(book, field, value)

    return book


# uvicorn start
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
