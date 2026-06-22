import uuid
import pytest
from pydantic import ValidationError
from db.config_test import open_test_session
from repositories.book import BookRepository
from schemas.book import BookCreate
from services.book import BookService


def test_create_book_success():
    with open_test_session() as db:
        service = BookService(db)

        result = service.register_new_book(BookCreate(title="Dune", author="Frank Herbert"))

        assert isinstance(result.id, uuid.UUID)
        assert result.title == "Dune"
        assert result.author == "Frank Herbert"


def test_create_book_persists_id():
    with open_test_session() as db:
        service = BookService(db)

        created = service.register_new_book(BookCreate(title="Dune", author="Frank Herbert"))

        repository = BookRepository(db)
        fetched = repository.get_book(created.id)

        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.title == "Dune"
        assert fetched.author == "Frank Herbert"


def test_create_book_rejects_empty_title():
    with pytest.raises(ValidationError):
        BookCreate(title="", author="Frank Herbert")


def test_create_book_rejects_oversized_title():
    with pytest.raises(ValidationError):
        BookCreate(title="A" * 101, author="Frank Herbert")


def test_create_two_books_get_distinct_ids():
    with open_test_session() as db:
        service = BookService(db)

        a = service.register_new_book(BookCreate(title="A", author="x"))
        b = service.register_new_book(BookCreate(title="B", author="y"))

        assert a.id != b.id
