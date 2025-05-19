from typing import AsyncGenerator
from pathlib import Path
import sys

sys.path[0] = str(Path(sys.path[0]).resolve().parent)

from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from httpx import AsyncClient, ASGITransport

import pytest

from src.routers.api.v1.auth.repository import UsersRepository
from src.routers.api.v1.auth.schemas import UserLoginSchema
from src.database.models import BooksOrm, ReadersOrm
from src.database.main import _get_session, Base
from src.utils.auth import create_access_token
from src.config import config
from src.main import app

engine = create_async_engine(config.db.test_url, poolclass=NullPool)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e


app.dependency_overrides[_get_session] = override_get_session


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    objects = [
        BooksOrm(title="Title 1", author="Author 1", amount=0),
        BooksOrm(title="Title 2", author="Author 1", amount=5),
        BooksOrm(title="Title 3", author="Author 2"),
        ReadersOrm(name="Name 1", email="name-1@example.com"),
    ]

    async with session_factory() as session:
        [session.add(obj) for obj in objects]
        repo = UsersRepository(session)
        await repo.create_user(
            UserLoginSchema(email="admin@example.com", password="12345678")
        )
        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


client = TestClient(app, "http://testserver/api/v1/")


@pytest.fixture(scope="session")
async def ac():
    """Async Client of app"""
    async with AsyncClient(
        transport=ASGITransport(app), base_url=client.base_url
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
async def aca():
    """Authorized Async Client of app"""
    async with AsyncClient(
        transport=ASGITransport(app), base_url=client.base_url
    ) as aca:
        async with session_factory() as session:
            repo = UsersRepository(session)
            user = await repo.get_user(email="admin@example.com")

        token = create_access_token(user)
        aca.headers["Authorization"] = f"Bearer {token}"
        yield aca
