from fastapi import HTTPException, status

BookIsNotAvailableException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='This book is not available'
)

TakingBookLimitException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='The reader cannot take more than 3 books'
)

ReaderDidNotTakeBookException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='The reader did not take this book'
)