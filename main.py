from fastapi import FastAPI
from fastapi import HTTPException
import uvicorn
from db import load_books, save_book
from sqlmodel import create_engine, SQLModel, Session, select

from schema import BookOutput,BookInput, Book

app = FastAPI(title="Book API", description="A simple API to manage books", version="1.0")

books = load_books()

engine = create_engine("sqlite:///books.db",
                       connect_args={"check_same_thread": False},
                       echo=True)

@app.on_event("startup")
def on_startup():
    """Create the database tables on startup."""
    SQLModel.metadata.create_all(engine)

@app.get("/api/books")
def get_books(genres: str|None = None, id_: int = None) -> list[Book]:
    """Get all books or filter by genres or id."""
    with Session(engine) as session:
        query = select(Book)
        if genres:
            query = query.where(Book.genres == genres)
        if id_ :
            query = query.where(Book.id_ == id_)
        return session.exec(query).all() # all 會把結果轉換成list 輸出

@app.get("/api/books/{id_}")
def get_book_by_id(id_: int) -> Book:
    """Get a book by its ID.""" 
    with Session(engine) as session:
        book = session.get(Book, id_)
        if book:
            return book
        else:
            raise HTTPException(status_code=404, detail=f"Not found id={id_} book")

@app.post("/api/books")
def add_book(book:BookInput) -> Book:
    with Session(engine) as session:
        new_book = Book.from_orm(book)
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
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