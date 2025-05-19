from fastapi import HTTPException, status

UserNotFoundException = lambda user_id: HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"User with id {user_id} not found",
)

NotUniqueUserException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User with same email is already exists",
)
