import json
from schema import BookOutput

def load_books() -> list:
    with open("books.json", "r", encoding="utf-8") as file:
        books = json.load(file)
    return [BookOutput(**book) for book in books]


def save_book(books:list[BookOutput]):
    with open("books.json","w",encoding="utf-8") as file:
        json.dump([book.model_dump() for book in books], file, indent=4,ensure_ascii=False)