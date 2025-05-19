from typing import Annotated

from fastapi import Depends, HTTPException, status

from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

from src.utils import get_current_user
from src.database.models import ReadersOrm

from .schemas import ReaderCreateSchema, ReaderUpdateSchema
from .exc import ReaderNotFoundException


class ReadersRepository:

    def __init__(self, user: get_current_user):
        self.user = user
        self.session = user.session

    async def create_reader(self, schema: ReaderCreateSchema) -> int:
        obj = ReadersOrm(**schema.model_dump())
        self.session.add(obj)

        try:
            await self.session.flush()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with same email is already exists",
            )

        return obj.id

    async def update_reader(self, schema: ReaderUpdateSchema) -> None:
        await self.get_reader(schema.id)

        stmt = (
            update(ReadersOrm)
            .where(ReadersOrm.id == schema.id)
            .values(**schema.model_dump())
        )

        await self.session.execute(stmt)

    async def get_reader(self, reader_id: int) -> ReadersOrm:
        if obj := await self.session.get(ReadersOrm, reader_id):
            return obj
        raise ReaderNotFoundException(reader_id)

    async def delete_reader(self, reader_id: int):
        reader = await self.get_book(reader_id)
        await self.session.delete(reader)


get_repository = Annotated[ReadersRepository, Depends(ReadersRepository)]
