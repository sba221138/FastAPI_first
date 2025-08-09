from sqlmodel import Field,SQLModel
    
class BookInput(SQLModel):
    title: str
    author: str
    publisher: str
    year_published: int
    isbn: str
    language: str
    pages: int
    genres: str
    summary: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Example Book",
                "author": "John Doe",
                "publisher": "Example Publisher",
                "year_published": 2023,
                "isbn": "123-4567890123",
                "language": "English",
                "pages": 300,
                "genres": "Fiction",
                "summary": "This is an example book summary."
            }
        }

class Book(BookInput, table=True):
    id_: int | None = Field(primary_key=True, default=None)

class BookOutput(BookInput):
    """Model for a book."""
    id_: int
    class Config:
        json_schema_extra = {
            "example": {
                "id_": 1,
                "title": "Example Book",
                "author": "John Doe",
                "publisher": "Example Publisher",
                "year_published": 2023,
                "isbn": "123-4567890123",
                "language": "English",
                "pages": 300,
                "genres": "Fiction",
                "summary": "This is an example book summary."
            }
        }

if __name__ == "__main__":
    book = BookInput(id_=10, title="test",author="aur",genres="小說",year_published=2023,isbn='123',language='中文',pages=300,summary='這是一本測試書籍。', publisher='測試出版社')
    print(book.model_dump())
    print(book.model_dump_json())
    print(book.id_)