from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth.jwt_ import get_current_token_payload, validate_token_type
from src.utils.auth.types import TokenType, Payload
from src.config import config

from src.database.models import UsersOrm
from src.database.main import _get_session


class UserGetterFromToken:

    def __init__(self, token_type: TokenType):
        self.token_type = token_type

    async def __call__(
        self,
        payload: Payload = Depends(get_current_token_payload),
        session: AsyncSession = Depends(_get_session),
    ) -> "UsersOrm":
        validate_token_type(payload, self.token_type)
        return await session.get(UsersOrm, payload["sub"])


get_current_user = Annotated[
    "UsersOrm",
    Depends(UserGetterFromToken(config.auth_jwt.access_token_type)),
]
get_current_user_for_refresh = Annotated[
    "UsersOrm",
    Depends(UserGetterFromToken(config.auth_jwt.refresh_token_type)),
]
