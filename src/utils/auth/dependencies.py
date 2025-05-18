from typing import Annotated, TYPE_CHECKING

from fastapi import Depends

from src.utils.auth.jwt_ import get_current_token_payload, validate_token_type
from src.utils.auth.types import TokenType, Payload
from src.utils.exc import UserNotFoundException
from src.repository import Crud
from src.config import config


if TYPE_CHECKING:
    from src.repository import User


class UserGetterFromToken:

    def __init__(self, token_type: TokenType):
        self.token_type = token_type

    async def __call__(
        self,
        payload: Payload = Depends(get_current_token_payload),
        crud: Crud = Depends(Crud),
    ) -> "User":
        validate_token_type(payload, self.token_type)
        user = await crud.get_user(id=payload["sub"])
        if user is None:
            raise UserNotFoundException
        return user


get_current_user = Annotated[
    "User",
    Depends(UserGetterFromToken(config.auth_jwt.access_token_type)),
]
get_current_user_for_refresh = Annotated[
    "User",
    Depends(UserGetterFromToken(config.auth_jwt.refresh_token_type)),
]
