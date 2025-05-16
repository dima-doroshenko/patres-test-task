from pydantic_settings import BaseSettings
from pydantic import BaseModel

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class App(BaseModel):
    title: str = "LibraryAPI"
    debug: bool = True


class DataBase(BaseModel):
    file: str = "database.db"
    driver: str = "sqlite+aiosqlite"

    @property
    def url(self) -> str:
        """URL для подключения SQLAlchemy"""
        return f"{self.driver}:///{self.file}"

    @property
    def abs_path(self) -> Path:
        """Абсолютный путь к файлу БД"""
        return BASE_DIR / self.file


class Settings(BaseSettings):
    app: App = App()
    db: DataBase = DataBase()


config = Settings()
