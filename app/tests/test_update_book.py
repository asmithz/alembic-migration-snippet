from uuid import uuid4
from db.config_test import open_test_session
from schemas.book import BookCreate, BookUpdate
from services.book import BookService


def test_update_book_title_only():
    with open_test_session() as db:
        service = BookService(db)
        created = service.register_new_book(BookCreate(title="Dune", author="Frank Herbert"))

        updated = service.update_book(created.id, BookUpdate(title="Dune (2nd ed.)"))

        assert updated is not None
        assert updated.id == created.id
        assert updated.title == "Dune (2nd ed.)"
        assert updated.author == "Frank Herbert"


def test_update_book_author_only():
    with open_test_session() as db:
        service = BookService(db)
        created = service.register_new_book(BookCreate(title="Dune", author="Frank Herbert"))

        updated = service.update_book(created.id, BookUpdate(author="F. Herbert"))

        assert updated is not None
        assert updated.id == created.id
        assert updated.title == "Dune"
        assert updated.author == "F. Herbert"


def test_update_book_both_fields():
    with open_test_session() as db:
        service = BookService(db)
        created = service.register_new_book(BookCreate(title="Dune", author="Frank Herbert"))

        updated = service.update_book(
            created.id, BookUpdate(title="Children of Dune", author="Frank Herbert")
        )

        assert updated is not None
        assert updated.id == created.id
        assert updated.title == "Children of Dune"
        assert updated.author == "Frank Herbert"


def test_update_unknown_book_returns_none():
    with open_test_session() as db:
        service = BookService(db)

        result = service.update_book(uuid4(), BookUpdate(title="Anything"))

        assert result is None
