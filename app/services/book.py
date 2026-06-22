from uuid import UUID

from sqlalchemy.orm import Session

from repositories.book import BookRepository
from schemas.book import BookCreate, BookOut, BookUpdate


class BookService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = BookRepository(self.db)

    def register_new_book(self, book_data: BookCreate) -> BookOut:
        book = self.repository.create_book(book_data)

        return BookOut.model_validate(book)

    def get_book(self, book_id: UUID) -> BookOut | None:
        book = self.repository.get_book(book_id)

        if not book:
            return None

        return BookOut.model_validate(book)

    def list_books(self) -> list[BookOut]:
        books = self.repository.list_books()

        return [BookOut.model_validate(book) for book in books]

    def update_book(self, book_id: UUID, payload: BookUpdate) -> BookOut | None:
        book = self.repository.update_book(book_id, payload)

        if not book:
            return None

        return BookOut.model_validate(book)

    def delete_book(self, book_id: UUID) -> bool:
        return self.repository.delete_book(book_id)
