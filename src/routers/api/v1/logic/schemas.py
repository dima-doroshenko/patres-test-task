from pydantic import BaseModel, EmailStr

from src.routers.api.v1.books.schemas import BookReadSchema


class ReaderInfo(BaseModel):
    name: str
    email: EmailStr
    borrowed_books: list[BookReadSchema]
