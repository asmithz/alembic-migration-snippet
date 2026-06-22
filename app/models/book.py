from sqlalchemy import String, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID
from db.config import Base


class Book(Base):
    __tablename__ = "book"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author: Mapped[str] = mapped_column(String(100))
