from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from src.database.models import UsersOrm
    from src.repository import User


class Properties:
    obj: "UsersOrm"

    @property
    def id(self: "User") -> int:
        return self.obj.id

    @property
    def email(self: "User") -> str:
        return self.obj.email

    @property
    def hashed_password(self: "User") -> bytes:
        return self.obj.hashed_password

    @property
    def created_at(self: "User") -> datetime:
        return self.obj.created_at
