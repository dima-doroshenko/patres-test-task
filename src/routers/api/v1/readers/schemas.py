from pydantic import BaseModel, Field, EmailStr

from src.schemas import OkResponse


class ReaderCreateSchema(BaseModel):
    name: str = Field(max_length=200)
    email: EmailStr = Field(max_length=50)


class ReaderReadSchema(BaseModel):
    name: str
    email: EmailStr


class ReaderUpdateSchema(ReaderCreateSchema):
    id: int = Field(gt=0)


class ReaderIdResponse(OkResponse):
    reader_id: int = Field(gt=0)
