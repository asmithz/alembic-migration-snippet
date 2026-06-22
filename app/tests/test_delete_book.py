from uuid import uuid4
from db.config_test import open_test_session
from schemas.book import BookCreate
from services.book import BookService


def test_delete_existing_book_returns_true_and_removes_it():
    with open_test_session() as db:
        service = BookService(db)
        created = service.register_new_book(BookCreate(title="Dune", author="Frank Herbert"))

        result = service.delete_book(created.id)

        assert result is True
        assert service.get_book(created.id) is None


def test_delete_unknown_book_returns_false():
    with open_test_session() as db:
        service = BookService(db)

        result = service.delete_book(uuid4())

        assert result is False


def test_deleted_book_absent_from_list():
    with open_test_session() as db:
        service = BookService(db)
        keep = service.register_new_book(BookCreate(title="Keep", author="a"))
        gone = service.register_new_book(BookCreate(title="Gone", author="b"))

        service.delete_book(gone.id)

        listed = service.list_books()
        print(listed)
        assert len(listed) == 1
        assert listed[0].id == keep.id
