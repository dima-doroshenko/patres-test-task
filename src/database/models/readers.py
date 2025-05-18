from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from src.database.anno import intpk
from src.database.main import Base

if TYPE_CHECKING:
    from src.database.models.borrowed_books import BorrowedBooksOrm
    from src.database.models.books import BooksOrm


class ReadersOrm(Base):
    __tablename__ = "readers"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(200), nullable=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)

    borrowed_book_records: Mapped[list["BorrowedBooksOrm"]] = relationship(
        back_populates="reader",
        lazy="selectin",
    )
