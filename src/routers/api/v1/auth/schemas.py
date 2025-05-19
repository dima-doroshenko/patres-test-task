from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserReadSchema(BaseModel):
    id: int = Field(ge=1)
    email: EmailStr
    created_at: datetime


__all__ = [
    "TokenInfo",
    "UserLoginSchema",
    "UserReadSchema",
]
