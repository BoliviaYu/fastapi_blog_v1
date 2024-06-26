from typing import Any, Generator
from functools import lru_cache

from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from jose import JWTError, jwt

from app import schemas
from app.config import settings, Settings
from app.db.session import SessionLocal

from .security import ALGORITHM, oauth2_scheme
from .users import get_user_by_username


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    except:
        raise
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> schemas.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
) -> schemas.User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@lru_cache
def get_settings() -> Settings:
    return Settings()
