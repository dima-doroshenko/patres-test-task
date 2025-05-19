from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.config import config


class Base(DeclarativeBase):

    def as_dict(self) -> dict[str]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


engine = create_async_engine(config.db.url)
session_factory = async_sessionmaker(
    engine, autoflush=config.db.autoflush, expire_on_commit=config.db.expire_on_commit
)


async def _get_session():
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e


get_session = Annotated[AsyncSession, Depends(_get_session)]
