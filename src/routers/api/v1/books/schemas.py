from pydantic import BaseModel, Field

from src.schemas import OkResponse


class BookCreateSchema(BaseModel):
    title: str = Field(max_length=200)
    author: str = Field(max_length=200)
    year: int | None = None
    isbn: str | None = Field(max_length=20, default=None)
    amount: int = Field(ge=0, default=1)


class BookReadSchema(BaseModel):
    id: int
    title: str
    author: str
    year: int | None
    isbn: str | None
    amount: int


class BookUpdateSchema(BaseModel):
    id: int = Field(gt=0)
    title: str | None = Field(None, max_length=200)
    author: str | None = Field(None, max_length=200)
    year: int | None = None
    isbn: str | None = Field(None, max_length=20)
    amount: int | None = Field(None, ge=0)


class BookIdResponse(OkResponse):
    book_id: int = Field(gt=0)
