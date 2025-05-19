from fastapi import HTTPException, status

ReaderNotFoundException = lambda book_id: HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Reader with id {book_id} not found",
)

NotUniqueReaderException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Reader with same email is already exists",
)
