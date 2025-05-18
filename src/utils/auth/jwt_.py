from datetime import timedelta, datetime, UTC
from typing import TYPE_CHECKING

from fastapi import Depends, HTTPException, status

from jwt import InvalidTokenError, ExpiredSignatureError
import jwt

from src.config import config
from src.utils.auth.meta import oauth2_scheme
from src.utils.exc import (
    InvalidTokenException,
    TokenExpiredException,
)
from src.utils.auth.types import Payload, TokenType

if TYPE_CHECKING:
    from src.repository import User


def encode_jwt(
    payload: Payload,
    private_key: str = config.auth_jwt.private_key_path.read_text(),
    algorithm: str = config.auth_jwt.algorithm,
    expire_minutes: int = config.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(UTC)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = config.auth_jwt.public_key_path.read_text(),
    algorithm: str = config.auth_jwt.algorithm,
):
    return jwt.decode(token, public_key, [algorithm])


def create_jwt(
    token_data: Payload,
    token_type: TokenType,
    expire_minutes: int = config.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {config.auth_jwt.token_type_field: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: "User") -> str:
    jwt_payload = {"sub": user.id}
    return create_jwt(
        token_data=jwt_payload,
        token_type=config.auth_jwt.access_token_type,
        expire_minutes=config.auth_jwt.access_token_expire_minutes,
    )


def create_refresh_token(user: "User") -> str:
    jwt_payload = {"sub": user.id}
    return create_jwt(
        token_data=jwt_payload,
        token_type=config.auth_jwt.refresh_token_type,
        expire_timedelta=timedelta(days=config.auth_jwt.refresh_token_expire_days),
    )


async def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> Payload:
    try:
        payload = decode_jwt(token)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except InvalidTokenError:
        raise InvalidTokenException
    return payload


def validate_token_type(payload: Payload, token_type: TokenType) -> bool:
    current_token_type = payload.get(config.auth_jwt.token_type_field)
    if current_token_type == token_type:
        return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid token type: expected {token_type!r}, get {current_token_type!r}",
    )
