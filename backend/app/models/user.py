from app.db.base import Base, timestamp

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
