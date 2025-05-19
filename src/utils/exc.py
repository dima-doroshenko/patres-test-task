"""HTTP Ошибки, которые используются чаще всего"""

from fastapi import HTTPException, status


UnauthedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid login or password",
)

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is invalid",
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
)
