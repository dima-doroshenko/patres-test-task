from pydantic_settings import BaseSettings
from pydantic import BaseModel

from pathlib import Path


BASEDIR = Path(__file__).resolve().parent.parent


class Library(BaseModel):
    book_borrowing_limit: int = 3


class App(BaseModel):
    title: str = "LibraryAPI"
    debug: bool = True


class DataBase(BaseModel):
    file: str = "database.db"
    driver: str = "sqlite+aiosqlite"

    autoflush: bool = False
    expire_on_commit: bool = False

    @property
    def url(self) -> str:
        """URL для подключения SQLAlchemy"""
        return f"{self.driver}:///{self.file}"

    @property
    def test_url(self) -> str:
        """URL для тестов"""
        return f"{self.driver}:///test_{self.file}"

    @property
    def abs_path(self) -> Path:
        """Абсолютный путь к файлу БД"""
        return BASEDIR / self.file

    @property
    def test_abs_path(self) -> Path:
        return BASEDIR / f"test_{self.file}"


class AuthJwt(BaseModel):
    private_key_path: Path = BASEDIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASEDIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    token_type_field: str = "type"
    access_token_type: str = "access"
    refresh_token_type: str = "refresh"


class Auth(BaseModel):
    token_url: str = "/api/v1/auth/login"


class Settings(BaseSettings):
    app: App = App()
    db: DataBase = DataBase()
    auth_jwt: AuthJwt = AuthJwt()
    auth: Auth = Auth()
    library: Library = Library()


config = Settings()
