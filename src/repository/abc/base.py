from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from src.repository import Crud


class BaseRepository[M]:
    crud: "Crud"
    session: AsyncSession
    obj: M | DeclarativeBase
