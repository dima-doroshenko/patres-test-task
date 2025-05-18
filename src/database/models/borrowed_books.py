from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.database.anno import intpk, created_date
from src.database.main import Base

if TYPE_CHECKING:
    from src.database.models.readers import ReadersOrm
    from src.database.models.books import BooksOrm


class BorrowedBooksOrm(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[intpk]
    reader_id: Mapped[int] = mapped_column(ForeignKey("readers.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    borrow_date: Mapped[created_date]
    return_date: Mapped[datetime] = mapped_column(nullable=True)
    
    reader: Mapped["ReadersOrm"] = relationship(lazy="joined")
    book: Mapped["BooksOrm"] = relationship(lazy="joined")
