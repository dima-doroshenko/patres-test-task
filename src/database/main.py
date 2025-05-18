from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import config


class Base(DeclarativeBase): ...


engine = create_async_engine(config.db.url)
session_factory = async_sessionmaker(engine, autoflush=config.db.autoflush, expire_on_commit=config.db.expire_on_commit)


async def get_session():
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
