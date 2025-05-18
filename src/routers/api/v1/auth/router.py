from fastapi import APIRouter, Depends

from src.repository import Crud, User
from src.utils import auth

from .utils import validate_auth_user
from .schemas import TokenInfo, UserLoginSchema

router = APIRouter()


@router.post("/register")
async def register(
    schema: UserLoginSchema,
    crud: Crud = Depends(Crud),
) -> TokenInfo:
    user = await crud.create_user(email=schema.email, password=schema.password)
    return login(user)

@router.post("/login")
def login(user: User = Depends(validate_auth_user)) -> TokenInfo:
    access_token = auth.create_access_token(user)
    refresh_token = auth.create_refresh_token(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model_exclude_none=True)
def refresh(user: auth.get_current_user_for_refresh) -> TokenInfo:
    access_token = auth.create_access_token(user)
    return TokenInfo(access_token=access_token)
