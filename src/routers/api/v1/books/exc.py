from fastapi import HTTPException, status

BookNotFoundException = lambda book_id: HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Book with id {book_id} not found",
)

NotUniqueBookException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Book with same title or ISBN is already exists",
)
