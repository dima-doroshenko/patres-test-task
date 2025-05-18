from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from config import config

http_bearer = HTTPBearer(auto_error=False)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.auth.token_url)
