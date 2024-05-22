from typing import List

from sqlalchemy.orm import Session

from app import models, schemas

from . import security


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def delete_user(db: Session, username: str) -> None:
    user = get_user_by_username(db=db, username=username)
    db.delete(user)
    db.commit()
    return None


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = security.get_hashed_password(user.password)
    user_data = user.model_dump()
    del user_data["password"]
    user_data["hashed_password"] = hashed_password
    user_post = models.User(**user_data)
    db.add(user_post)
    db.commit()
    db.refresh(user_post)
    return user_post


def update_user(db: Session, user: schemas.UserUpdate, username: str) -> models.User:
    db_user = get_user_by_username(db=db, username=username)
    user_data = user.model_dump()
    new_password = user_data.get("password")
    if new_password:
        new_hashed_password = security.get_hashed_password(new_password)
        db_user.hashed_password = new_hashed_password
    db_user.username = user_data.get("username")
    db_user.profile = user_data.get("profile")
    db_user.email = user_data.get("email")
    db_user.disabled = user_data.get("disabled")

    db.commit()
    db.refresh(db_user)
    return db_user
