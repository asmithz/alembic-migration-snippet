from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BookBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    author: str | None = Field(default=None, min_length=1, max_length=100)


class BookOut(BookBase):
    id: UUID