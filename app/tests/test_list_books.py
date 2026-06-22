from db.config_test import open_test_session
from schemas.book import BookCreate
from services.book import BookService


def test_list_books_empty_initially():
    with open_test_session() as db:
        service = BookService(db)

        assert service.list_books() == []


def test_list_books_returns_all_created():
    with open_test_session() as db:
        service = BookService(db)
        a = service.register_new_book(BookCreate(title="A", author="x"))
        b = service.register_new_book(BookCreate(title="B", author="y"))
        c = service.register_new_book(BookCreate(title="C", author="z"))

        result = service.list_books()

        assert len(result) == 3
        ids = {book.id for book in result}
        assert ids == {a.id, b.id, c.id}