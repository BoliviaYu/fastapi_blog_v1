from typing import Optional, Any
from datetime import datetime

from pydantic import BaseModel, field_validator, StrictBool


class UserBase(BaseModel):
    username: str
    profile: str
    email: str
    disabled: StrictBool = False


class UserCreate(UserBase):
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, username: str) -> str:
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return username

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str) -> str:
        if len(email) == 0:
            raise ValueError("Email cannot be empty")
        return email

    @field_validator("profile")
    @classmethod
    def validate_profile(cls, profile: str) -> str:
        if len(profile) == 0:
            raise ValueError("A profile is required")
        return profile


class User(UserBase):
    id: Optional[int] = None


class UserInDB(User):
    hashed_password: str


class UserOutDB(User):
    id: int
    created_at: datetime
    updated_at: datetime


class Users(User):
    id: int


class UserUpdate(UserBase):
    password: Optional[str]


class UserPassword(BaseModel):
    password: Optional[str] = None
