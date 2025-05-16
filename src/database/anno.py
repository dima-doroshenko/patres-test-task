from typing import Annotated
from datetime import datetime, UTC

from sqlalchemy.orm import mapped_column

intpk = Annotated[int, mapped_column(primary_key=True)]

created_at = Annotated[
    datetime, mapped_column(default_factory=lambda: datetime.now(UTC))
]

created_date = Annotated[
    datetime, mapped_column(default_factory=lambda: datetime.now(UTC).date())
]
