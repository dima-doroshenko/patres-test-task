from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import UsersOrm
from src.repository.user import User
from src.database import get_session


class Crud:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_user(self, id: int) -> User | None:
        if obj := await self.session.get(UsersOrm, id):
            return User(self, obj)
