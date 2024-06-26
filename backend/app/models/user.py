from enum import Enum

from app.db.base import Base, create_time, update_time

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Text, Enum as SQLEnum


class UserRole(str, Enum):
    admin = "admin"
    visitor = "visitor"
    user = "user"
    super_admin = "super_admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(30), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(128))
    profile: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(
        SQLEnum(UserRole), default=UserRole.visitor, nullable=False
    )
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[create_time]
    updated_at: Mapped[update_time]
