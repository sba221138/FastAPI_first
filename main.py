from fastapi import FastAPI
from fastapi import HTTPException
import uvicorn
import db
app = FastAPI()

books = db.load_books()

@app.get("/api/books")
def get_books(genres: str|None = None, _id: str|int = None) -> list:
    """Get all books or filter by genres or id."""
    result = books
    if genres:
        return [book for book in books if book["genres"] == genres]
    if _id:
        return next((book for book in books if book["_id"] == _id), None)
    return result

@app.get("/api/books/{_id}")
def get_book_by_id(_id: int) -> dict:
     """Get a book by its ID."""
     result = [book for book in books if book["_id"] == _id]
     if result:
         return result[0]
     raise HTTPException(status_code=404, detail=f"Not found id={_id} book")
    
if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)