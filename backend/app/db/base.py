import datetime

from typing import Annotated

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy import func


class Base(DeclarativeBase):
    pass


create_time = Annotated[
    datetime.datetime,
    mapped_column(
        nullable=False,
        server_default=func.now(),
    ),
]

update_time = Annotated[
    datetime.datetime,
    mapped_column(
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
]
