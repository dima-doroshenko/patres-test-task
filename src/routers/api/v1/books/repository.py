from typing import Annotated

from fastapi import Depends

from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, select

from src.database.models import BooksOrm
from src.utils import get_current_user
from src.database import get_session

from .exc import BookNotFoundException, NotUniqueBookException
from .schemas import BookCreateSchema, BookUpdateSchema


class BooksRepository:

    def __init__(self, user: get_current_user, session: get_session):
        self.user = user
        self.session = session

    async def create_book(self, schema: BookCreateSchema) -> int:
        obj = BooksOrm(**schema.model_dump())
        self.session.add(obj)
        try:
            await self.session.flush()
        except IntegrityError:
            raise NotUniqueBookException

        return obj.id

    async def update_book(self, schema: BookUpdateSchema) -> None:
        await self.get_book(schema.id)

        stmt = (
            update(BooksOrm)
            .where(BooksOrm.id == schema.id)
            .values(**schema.model_dump())
        )

        await self.session.execute(stmt)

    async def get_book(self, book_id: int) -> BooksOrm:
        if obj := await self.session.get(BooksOrm, book_id):
            return obj
        raise BookNotFoundException(book_id)

    async def get_all_books(self, limit: int, offset: int) -> list[BooksOrm]:
        query = select(BooksOrm).limit(limit).offset(offset)
        return await self.session.scalars(query)

    async def delete_book(self, book_id: int):
        book = await self.get_book(book_id)
        await self.session.delete(book)


get_repository = Annotated[BooksRepository, Depends(BooksRepository)]
