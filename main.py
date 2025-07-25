from fastapi import FastAPI
from fastapi import HTTPException
import uvicorn
from db import load_books, save_book
from schema import BookOutput,BookInput

app = FastAPI(title="Book API", description="A simple API to manage books", version="1.0")

books = load_books()

@app.get("/api/books")
def get_books(genres: str|None = None, id_: int = None) -> list[BookOutput]:
    """Get all books or filter by genres or id."""
    result = books
    if genres:
        return [book for book in result if book.genres == genres]
    if id_:
        return [book for book in result if book.id_ == id_]
    return result

@app.get("/api/books/{id_}")
def get_book_by_id(id_: int) -> BookOutput:
     """Get a book by its ID."""
     result = [book for book in books if book.id_ == id_]
     if result:
        return result[0]
     raise HTTPException(status_code=404, detail=f"Not found id={id_} book")

@app.post("/api/books")
def add_book(book:BookInput) -> BookOutput:
    max_id = max((book.id_ for book in books), default=0)
    new_book = BookOutput(
        id_=max_id + 1,  # Simple ID generation
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        year_published=book.year_published,
        isbn=book.isbn,
        language=book.language,
        pages=book.pages,
        genres=book.genres,
        summary=book.summary
    )
    books.append(new_book)
    save_book(books)
    return new_book

@app.delete("/api/books/{id_}")
def delete_book(id_:int):
    match_book = [book for book in books if book.id_ == id_]
    if match_book:
        books.remove(match_book[0])
        save_book(books)
    raise HTTPException(status_code=404, detail=f"Not found id={id_} book")

@app.put("/api/books/{id_}")
def update_book(id_:int, new_book:BookInput) -> BookOutput:
    match_book = [book for book in books if book.id_ == id_]
    if match_book:
        book = match_book[0]
        book.title = new_book.title
        book.author = new_book.author
        book.publisher = new_book.publisher
        book.year_published = new_book.year_published
        book.isbn = new_book.isbn
        book.language = new_book.language
        book.pages = new_book.pages
        book.genres = new_book.genres
        book.summary = new_book.summary
        save_book(books)
        return book 
    raise HTTPException(status_code=404, detail=f"Not found id={id_} book")

if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)