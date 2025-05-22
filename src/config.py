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
    user: str = "postgres"
    password: str = "postgres"
    host: str = "postgres"
    port: int = 5432
    dbname: str = "postgres"

    driver: str = "postgresql+asyncpg"
    autoflush: bool = False
    expire_on_commit: bool = False

    @property
    def url(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

    @property
    def test_url(self) -> str:
        return f"sqlite+aiosqlite:///test_database.db"


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
