from fastapi import APIRouter

router = APIRouter(prefix='/v1')

from .auth import router as auth_router
router.include_router(
    auth_router,
    prefix='/auth',
    tags=['Auth']
)