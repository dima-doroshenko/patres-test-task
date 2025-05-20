from httpx import AsyncClient

import pytest


@pytest.mark.parametrize(
    "url, method",
    [
        ("/readers/1", "get"),
        ("/books/1", "get"),
        ("/auth/me", "get"),
        ("/logic/borrow", "post"),
    ],
)
async def test_protected(url: str, method: str, ac: AsyncClient):
    response = await ac.request(method, url)
    assert response.status_code == 401


async def test_protected_with_auth(aca: AsyncClient):
    response = await aca.get("/auth/me")
    assert response.status_code == 200
