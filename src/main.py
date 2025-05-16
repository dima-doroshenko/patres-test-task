from fastapi import FastAPI

from src.config import config

app = FastAPI(
    debug=config.app.debug,
    title=config.app.title,
)
