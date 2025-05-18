from pydantic_settings import BaseSettings
from pydantic import BaseModel

from pathlib import Path

from src.utils.auth import types as AuthTypes

BASEDIR = Path(__file__).resolve().parent


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
    def abs_path(self) -> Path:
        """Абсолютный путь к файлу БД"""
        return BASEDIR / self.file


class AuthJwt(BaseModel):
    private_key_path: Path = BASEDIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASEDIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 30

    token_type_field: str = "type"
    access_token_type: AuthTypes.TokenType = "access"
    refresh_token_type: AuthTypes.TokenType = "refresh"


class Auth(BaseModel):
    token_url: str = "/api/v1/auth/login"


class Settings(BaseSettings):
    app: App = App()
    db: DataBase = DataBase()
    auth_jwt: AuthJwt = AuthJwt()
    auth: Auth = Auth()


config = Settings()
