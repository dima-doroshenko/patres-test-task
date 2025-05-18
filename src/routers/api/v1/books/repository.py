from typing import Annotated

from fastapi import HTTPException, status, Depends

from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, select, delete

from src.database.models import BooksOrm
from src.utils import get_current_user

from .schemas import BookCreateSchema, BookUpdateSchema
from .exc import BookNotFoundException


class Repository:

    def __init__(self, user: get_current_user):
        self.user = user
        self.session = user.session

    async def create_book(self, schema: BookCreateSchema) -> int:
        obj = BooksOrm(**schema.model_dump())
        self.session.add(obj)
        try:
            await self.session.flush()
        except Exception as err:
            if "UNIQUE" in str(err):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Book with same title or ISBN is already exists",
                )
            raise err

        return obj.id

    async def update_book(self, schema: BookUpdateSchema) -> None:

        await self.get_book(schema.id)

        stmt = (
            update(BooksOrm)
            .where(BooksOrm.id == schema.id)
            .values(**schema.model_dump())
        )

        try:
            await self.session.execute(stmt)
        except Exception as err:
            raise BookNotFoundException(44)

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


get_repository = Annotated[Repository, Depends(Repository)]
