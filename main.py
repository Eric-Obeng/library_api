from fastapi import FastAPI

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "The Pragmatic Programmer",
        "author": "Hunt",
        "category": "programming",
    },
    {"id": 2, "title": "Clean Code", "author": "Martin", "category": "programming"},
    {"id": 3, "title": "1984", "author": "Orwell", "category": "fiction"},
]


# A. Root Endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Library API!"}


# B. Get Book by ID
@app.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    if book_id < 0:
        return {"error": "Invalid book ID."}

    for book in books:
        if book["id"] == book_id:
            return book

    return {"error": "Book not found."}


# C. Search for Books
@app.get("/search")
def search_books(title: str = None, author: str = None, limit: int = 5):
    search_results = books

    if title:
        search_results = [
            book for book in search_results if title.lower() in book["title"].lower()
        ]

    if author:
        search_results = [
            book for book in search_results if author.lower() in book["author"].lower()
        ]

    search_results = search_results[:limit]

    if not search_results:
        return {"results": [], "message": "No books found."}

    return {"results": search_results, "count": len(search_results)}


# D. Filter Books by Category
@app.get("/category/{category_name}")
def filter_book_by_category(category_name: str, sort: str = None):
    filtered_book = [
        book for book in books if book["category"].lower() == category_name.lower()
    ]

    if sort:
        sort_lower = sort.lower()
        if sort_lower not in ("asc", "desc"):
            return {"error": "Invalid sort value. User 'asc' or 'desc'."}
        reverse = sort_lower == "desc"
        filtered_book.sort(key=lambda b: b["title"].lower(), reverse=reverse)

    if not filtered_book:
        return {"results": [], "message": "No books found."}

    return {"result": filtered_book, "count": len(filtered_book)}


# uvicorn start
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
