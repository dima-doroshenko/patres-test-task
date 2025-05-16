from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

from src.database.anno import intpk, created_date
from src.database.main import Base


class BorrowedBooksOrm(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    borrow_date: Mapped[created_date]
    return_date: Mapped[datetime] = mapped_column(nullable=True)
