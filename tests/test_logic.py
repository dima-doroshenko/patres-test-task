from httpx import AsyncClient

import pytest

from src.config import config


async def test_business_logic_1(aca: AsyncClient):
    response = await aca.post("/logic/borrow", params={"book_id": 1, "reader_id": 1})
    assert response.status_code == 400
    assert "is not available" in response.json()["detail"]


async def test_business_logic_2(aca: AsyncClient):

    BOOK_ID = 2
    READER_ID = 1

    async def _borrow():
        return await aca.post(
            "/logic/borrow", params={"book_id": BOOK_ID, "reader_id": READER_ID}
        )

    for _ in range(config.library.book_borrowing_limit):
        await _borrow()

    response = await _borrow()

    assert response.status_code == 400
    assert "cannot take more than" in response.json()["detail"]

    for _ in range(config.library.book_borrowing_limit):
        await aca.post(
            "/logic/return", params={"book_id": BOOK_ID, "reader_id": READER_ID}
        )


@pytest.mark.parametrize("book_id", [3, 2])
async def test_business_logic_3(book_id: int, aca: AsyncClient):
    response = await aca.post(
        "/logic/return", params={"book_id": book_id, "reader_id": 1}
    )
    assert response.status_code == 400
    assert "did not take" in response.json()["detail"]
