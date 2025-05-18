from pydantic import BaseModel

class OkResponse(BaseModel):
    ok: bool = True

class ExceptionResponse(BaseModel):
    ok: bool = False
    status: int = 400
    detail: str | None = None
