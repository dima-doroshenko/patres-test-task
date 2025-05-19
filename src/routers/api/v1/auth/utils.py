from fastapi import Form, Depends

from src.repository import Crud
from src.utils import UnauthedException


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    crud: Crud = Depends(Crud),
):
    user = await crud.get_user_by_email(username)
    if (not user) or (not user.check_password(password)):
        raise UnauthedException
    return user
