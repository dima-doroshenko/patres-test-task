"""HTTP Ошибки, которые используются чаще всего"""

from fastapi import HTTPException, status


UnauthedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid login or password",
)

UserNotFoundException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User not found",
)

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token is invalid",
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
)

ThisUsernameIsAlreadyTaken = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="User with same username already exists",
)

ThisEmailIsAlreadyTaken = HTTPException(
    status.HTTP_400_BAD_REQUEST,
    detail="User with same email already exists",
)
