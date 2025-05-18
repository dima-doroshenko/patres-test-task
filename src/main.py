from fastapi import FastAPI

from src.config import config
from src.routers import router

app = FastAPI(
    debug=config.app.debug,
    title=config.app.title,
)

app.include_router(router)
