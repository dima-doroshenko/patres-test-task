from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, CheckConstraint

from src.database.anno import intpk
from src.database.main import Base


class BooksOrm(Base):
    __tablename__ = "books"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(200), unique=True)
    author: Mapped[str] = mapped_column(String(200))
    year: Mapped[int] = mapped_column(nullable=True)
    isbn: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    description: Mapped[str] = mapped_column(String(2000), default="")
    amount: Mapped[int] = mapped_column(default=1)

    __table_args__ = (
        CheckConstraint("amount >= 0"),
    )
