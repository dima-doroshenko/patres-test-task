from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class _Password(BaseModel):
    password: str = Field(min_length=8)


class _Email(BaseModel):
    email: EmailStr


class _ID(BaseModel):
    id: int = Field(ge=1)


class UserLoginSchema(_Password, _Email): ...


class UserReadSchema(_Email, _ID):
    created_at: datetime


__all__ = [
    "TokenInfo",
    "UserLoginSchema",
    "UserReadSchema",
]
