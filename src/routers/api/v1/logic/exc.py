from fastapi import HTTPException, status

from src.config import config

BookIsNotAvailableException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="This book is not available",
)

TakingBookLimitException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=f"The reader cannot take more than {config.library.book_borrowing_limit} books",
)

ReaderDidNotTakeBookException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The reader has not taken this book or has already returned it",
)
