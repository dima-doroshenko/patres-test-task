from fastapi import HTTPException, status

ReaderNotFoundException = lambda reader_id: HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail=f"Reader with id {reader_id} not found",
)

NotUniqueReaderException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Reader with same email is already exists",
)
