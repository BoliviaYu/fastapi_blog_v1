from app.db.base import Base, timestamp

# from app.db.base import Base, timestamp

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[timestamp]
