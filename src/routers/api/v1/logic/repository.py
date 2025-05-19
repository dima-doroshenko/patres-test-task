from typing import Annotated
from datetime import datetime, UTC

from fastapi import Depends

from sqlalchemy import select

from src.database.models import BorrowedBooksOrm, BooksOrm
from src.utils import get_current_user
from src.config import config

from src.routers.api.v1.readers.repository import ReadersRepository
from src.routers.api.v1.books.repository import BooksRepository
from src.routers.api.v1.books.schemas import BookReadSchema

from .schemas import ReaderInfo
from .exc import (
    TakingBookLimitException,
    BookIsNotAvailableException,
    ReaderDidNotTakeBookException,
)


class LogicReposiory:

    def __init__(self, user: get_current_user):
        self.user = user
        self.session = user.session

    async def _get_book(self, id: int):
        return await BooksRepository(self.user).get_book(id)

    async def _get_reader(self, id: int):
        return await ReadersRepository(self.user).get_reader(id)

    async def borrow_book(self, book_id: int, reader_id: int) -> None:
        reader = await self._get_reader(reader_id)

        amount_of_not_returned_books = len(
            [r for r in reader.borrowed_book_records if not r.return_date]
        )

        if amount_of_not_returned_books >= config.library.book_borrowing_limit:
            raise TakingBookLimitException

        book = await self._get_book(book_id)

        if book.amount == 0:
            raise BookIsNotAvailableException

        obj = BorrowedBooksOrm(book_id=book_id, reader_id=reader_id)
        self.session.add(obj)
        
        book.amount -= 1

    async def return_book(self, book_id: int, reader_id: int) -> None:

        reader = await self._get_reader(reader_id)
        book = await self._get_book(book_id)

        query = (
            select(BorrowedBooksOrm)
            .where(BorrowedBooksOrm.book_id == book_id)
            .where(BorrowedBooksOrm.reader_id == reader_id)
            .where(BorrowedBooksOrm.return_date == None)
        )

        objects = list(await self.session.scalars(query))

        if not len(objects):
            raise ReaderDidNotTakeBookException

        objects[0].return_date = datetime.now(UTC).date()
        book.amount += 1

    async def info_about_reader(self, reader_id: int) -> ReaderInfo:
        reader = await self._get_reader(reader_id)

        query = select(BooksOrm).where(
            BooksOrm.id.in_(
                [r.book_id for r in reader.borrowed_book_records if not r.return_date]
            )
        )

        res = await self.session.scalars(query)

        return ReaderInfo(
            name=reader.name,
            email=reader.email,
            borrowed_books=[BookReadSchema(**book.as_dict()) for book in res.all()],
        )


get_repository = Annotated[LogicReposiory, Depends(LogicReposiory)]
