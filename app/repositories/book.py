from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.book import Book
from schemas.book import BookCreate, BookUpdate


class BookRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_book(self, data: BookCreate) -> Book:
        book = Book(
            id=uuid4(), 
            title=data.title, 
            author=data.author
        )

        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)

        return book

    def get_book(self, book_id: UUID) -> Book | None:
        return self.db.get(Book, book_id)

    def list_books(self) -> list[Book]:
        stmt = (select(Book))
        return list(self.db.execute(stmt).scalars().all())

    def update_book(self, book_id: UUID, payload: BookUpdate) -> Book | None:
        book = self.db.get(Book, book_id)

        if book is None:
            return None

        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(book, key, value)

        self.db.commit()
        self.db.refresh(book)

        return book

    def delete_book(self, book_id: UUID) -> bool:
        book = self.db.get(Book, book_id)

        if book is None:
            return False

        self.db.delete(book)
        self.db.commit()

        return True
