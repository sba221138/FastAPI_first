import json
def load_books() -> list:
    with open("books.json", "r", encoding="utf-8") as file:
        return json.load(file)