from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from src.config import config
from src.routers import router
from src.schemas import ExceptionResponse

app = FastAPI(
    debug=config.app.debug,
    title=config.app.title,
)


@app.exception_handler(HTTPException)
async def handle_httpexception(request: Request, exc: HTTPException):
    return JSONResponse(
        ExceptionResponse(status=exc.status_code, detail=exc.detail).model_dump(),
        status_code=exc.status_code,
    )


app.include_router(router)
