from fastapi import APIRouter, Depends

from src.schemas import OkResponse

from .schemas import BookCreateSchema, BookReadSchema, BookUpdateSchema, BookIdResponse
from .repository import get_repository

router = APIRouter()


@router.post("/")
async def create_book(repo: get_repository, schema: BookCreateSchema) -> BookIdResponse:
    book_id = await repo.create_book(schema)
    return BookIdResponse(book_id=book_id)


@router.get("/{id}")
async def get_book(repo: get_repository, id: int) -> BookReadSchema:
    return await repo.get_book(id)


@router.get("/")
async def get_all_books(
    repo: get_repository, limit: int = 50, offset: int = 0
) -> list[BookReadSchema]:
    return await repo.get_all_books(limit, offset)


@router.put("/")
async def update_book(repo: get_repository, schema: BookUpdateSchema) -> OkResponse:
    await repo.update_book(schema)
    return OkResponse


@router.delete("/{id}")
async def delete_book(repo: get_repository, id: int) -> OkResponse:
    await repo.delete_book(id)
    return OkResponse
