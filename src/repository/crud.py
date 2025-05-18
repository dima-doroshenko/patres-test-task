from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.models import UsersOrm
from src.repository.user import User
from src.utils.auth import hash_password
from src.utils.exc import ThisEmailIsAlreadyTaken
from src.database import get_session


class Crud:

    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def get_user(self, id: int) -> User | None:
        if obj := await self.session.get(UsersOrm, id):
            return User(self, obj)

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(UsersOrm).where(UsersOrm.email == email)
        if (obj := await self.session.scalar(query)):
            return User(self, obj)

    async def create_user(self, email: str, password: str) -> User:
        hashed_password = hash_password(password)
        obj = UsersOrm(email=email, hashed_password=hashed_password)
        self.session.add(obj)
        try:
            await self.session.flush()
        except:
            raise ThisEmailIsAlreadyTaken
        return obj
