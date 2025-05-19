from fastapi import APIRouter, Depends

from src.database.models import UsersOrm
from src.utils import auth

from .schemas import TokenInfo, UserLoginSchema, UserReadSchema
from .repository import get_repository
from .utils import validate_auth_user

router = APIRouter()


@router.post("/register")
async def register(
    repo: get_repository,
    schema: UserLoginSchema,
) -> TokenInfo:
    user = await repo.create_user(email=schema.email, password=schema.password)
    return login(user)


@router.post("/login")
def login(user: UsersOrm = Depends(validate_auth_user)) -> TokenInfo:
    access_token = auth.create_access_token(user)
    refresh_token = auth.create_refresh_token(user)
    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model_exclude_none=True)
def refresh(user: auth.get_current_user_for_refresh) -> TokenInfo:
    access_token = auth.create_access_token(user)
    return TokenInfo(access_token=access_token)


@router.get("/me")
async def get_me(user: auth.get_current_user, repo: get_repository) -> UserReadSchema:
    return await repo.get_user(user.id)
