from fastapi import APIRouter

from .schemas import ReaderInfo

router = APIRouter()

from src.schemas import OkResponse

from .repository import get_repository


@router.post("/borrow")
async def borrow_book(repo: get_repository, book_id: int, reader_id: int) -> OkResponse:
    await repo.borrow_book(book_id, reader_id)
    return OkResponse()


@router.post("/return")
async def return_book(repo: get_repository, book_id: int, reader_id: int) -> OkResponse:
    await repo.return_book(book_id, reader_id)
    return OkResponse()


@router.get("/info/{reader_id}")
async def get_info_about_reader(repo: get_repository, reader_id: int) -> ReaderInfo:
    return await repo.info_about_reader(reader_id)
