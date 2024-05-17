from typing import Optional, Any

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
    def validate_email(cls, email: Any) -> str:
        if len(email == 0):
            raise ValueError("Email cannot be empty")
        return email
    
    @field_validator("password")
    @classmethod
    