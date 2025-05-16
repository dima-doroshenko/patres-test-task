from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.database.anno import created_at, intpk
from src.database.main import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    email: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[bytes]
    created_at: Mapped[created_at]
