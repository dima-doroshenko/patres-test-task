from typing import Annotated

from fastapi import Depends

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from src.utils.auth import hash_password
from src.database.models import UsersOrm
from src.database import get_session

from .exc import NotUniqueUserException, UserNotFoundException
from .schemas import UserLoginSchema


class UsersRepository:

    def __init__(self, session: get_session):
        self.session = session

    async def get_user(self, **filter_by) -> UsersOrm:
        query = select(UsersOrm).filter_by(**filter_by)
        if obj := await self.session.scalar(query):
            return obj
        raise UserNotFoundException

    async def create_user(self, schema: UserLoginSchema) -> UsersOrm:
        hashed_password = hash_password(schema.password)

        obj = UsersOrm(email=schema.email, hashed_password=hashed_password)
        self.session.add(obj)

        try:
            await self.session.flush()
        except IntegrityError:
            raise NotUniqueUserException

        return obj


get_repository = Annotated[UsersRepository, Depends(UsersRepository)]
