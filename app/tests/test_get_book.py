from uuid import uuid4
from db.config_test import open_test_session
from schemas.book import BookCreate
from services.book import BookService


def test_get_existing_book_returns_book_out():
    with open_test_session() as db:
        service = BookService(db)
        created = service.register_new_book(BookCreate(title="Dune", author="Frank Herbert"))

        fetched = service.get_book(created.id)

        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.title == "Dune"
        assert fetched.author == "Frank Herbert"


def test_get_unknown_book_returns_none():
    with open_test_session() as db:
        service = BookService(db)

        result = service.get_book(uuid4())

        assert result is None
