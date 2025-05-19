from fastapi import Form, Depends

from src.routers.api.v1.auth.repository import UsersRepository
from src.utils.auth import check_password
from src.utils import UnauthedException


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    repo: UsersRepository = Depends(UsersRepository),
):
    user = await repo.get_user(email=username)
    if (not user) or (not check_password(password, user.hashed_password)):
        raise UnauthedException
    return user
