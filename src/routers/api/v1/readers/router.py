from fastapi import APIRouter

from src.schemas import OkResponse

from .repository import get_repository
from .schemas import (
    ReaderCreateSchema,
    ReaderReadSchema,
    ReaderUpdateSchema,
    ReaderIdResponse,
)

router = APIRouter()


@router.post("/")
async def create_rereader(
    repo: get_repository, schema: ReaderCreateSchema
) -> ReaderIdResponse:
    reader_id = await repo.create_reader(schema)
    return ReaderIdResponse(reader_id=reader_id)


@router.get("/{id}")
async def get_reader(repo: get_repository, id: int) -> ReaderReadSchema:
    return await repo.get_reader(id)


@router.put("/")
async def update_reader(repo: get_repository, schema: ReaderUpdateSchema) -> OkResponse:
    await repo.update_reader(schema)
    return OkResponse()


@router.delete("/{int}")
async def delete_reader(repo: get_repository, id: int) -> OkResponse:
    await repo.delete_reader(id)
    return OkResponse()
