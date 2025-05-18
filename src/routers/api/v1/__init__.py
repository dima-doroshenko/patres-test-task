from fastapi import APIRouter

router = APIRouter(prefix="/v1")


from .auth import router as auth_router

router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Auth"],
)

from .books import router as books_router

router.include_router(
    books_router,
    prefix="/books",
    tags=["Books"],
)
