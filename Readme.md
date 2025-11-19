# Library API

Small example API built with FastAPI that serves a tiny in-memory collection of books.

## Features

- Minimal endpoints for learning and experimentation
- In-memory data (no database required)
- Search, category filtering and optional sorting

## Endpoints

- `GET /` — Welcome message
- `GET /books/{book_id}` — Retrieve a single book by its integer ID
- `GET /search` — Query books by `title` and/or `author`. Optional `limit` query param.
- `GET /category/{category_name}` — List books in a category. Optional `sort` query param: `asc` or `desc` (alphabetical by title)

## Quick Start (Windows PowerShell)

1. Create and activate a virtual environment (recommended)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

1. Install dependencies

```powershell
pip install fastapi uvicorn
```

1. Run the server

```powershell
python main.py
```

1. Open the interactive docs in your browser

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Examples

- Get welcome: `curl http://127.0.0.1:8000/`
- Get book id 2: `curl http://127.0.0.1:8000/books/2`
- Search titles: `curl "http://127.0.0.1:8000/search?title=Code"`
- Category sorted asc: `curl "http://127.0.0.1:8000/category/programming?sort=asc"`
