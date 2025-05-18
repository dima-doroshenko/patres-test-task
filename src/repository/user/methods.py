from typing import TYPE_CHECKING


from src.utils.auth import check_password

if TYPE_CHECKING:
    from src.repository import User


class Methods:

    def check_password(self: "User", password: str):
        return check_password(password, self.obj.hashed_password)
