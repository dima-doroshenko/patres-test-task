from fastapi import HTTPException, status

ReaderNotFoundException = lambda book_id: HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Reader with id {book_id} not found",
)
