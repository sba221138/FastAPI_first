from pydantic import BaseModel

class Book(BaseModel):
    """Model for a book."""
    _id: int
    title: str
    author: str
    publisher: str
    year_published: int
    isbn: str
    language: str
    pages: int
    genres: str
    summary: str

if __name__ == "__main__":
    book = Book(_id=10, title="test",author="aur",genres="小說",year_published=2023,)
