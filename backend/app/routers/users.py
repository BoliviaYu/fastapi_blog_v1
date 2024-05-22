from datetime import timedelta
from typing import Any, List, Optional

from fastapi import Depends, HTTPException, Response, status
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from sqlalchemy.orm import Session

from app import schemas, models
from app.services import (
    authenticate_user,
    create_access_token,
    create_user,
    get_current_active_user,
    get_db,
    get_user_by_email,
    get_user_by_id,
    get_user_by_username,
    delete_user,
    get_users,
    update_user,
)
from app.services.security import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/users",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_new_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    db_username = get_user_by_username(db=db, username=user.username)
    db_email = get_user_by_email(db=db, email=user.email)
    if db_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    elif db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user(db=db, user=user)


@router.get(
    "/users",
    response_model=Page[schemas.User],
    status_code=status.HTTP_200_OK,
    summary="Get all users by pagination",
)
def get_all_users_by_pagination(
    db: Session = Depends(get_db),
) -> Any:
    return paginate(db.query(models.User))


@router.get(
    "/all_users",
    response_model=List[schemas.User],
    status_code=status.HTTP_200_OK,
    summary="Get all users",
)
def get_all_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> List[schemas.UserOutDB]:
    return get_users(db=db, skip=skip, limit=limit)


@router.get(
    "/users/user",
    response_model=schemas.UserOutDB,
    status_code=status.HTTP_200_OK,
    summary="Get user by id or name",
)
def read_user(
    db: Session = Depends(get_db),
    user_id: Optional[int] = None,
    username: Optional[str] = None,
) -> schemas.UserOutDB:
    if user_id:
        user = get_user_by_id(db=db, user_id=user_id)
    elif username:
        user = get_user_by_username(db=db, username=username)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.put(
    "/user/{username}",
    response_model=schemas.User,
    status_code=status.HTTP_200_OK,
    summary="Update user by name",
)
def update_user_by_username(
    username: str,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
) -> schemas.User:
    if username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to update this user",
        )
    result = update_user(db=db, user=user, username=username)
    return result


@router.post(
    "/token",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK,
    summary="Get access token",
)
def login_for_access_token(
    response: Response = None,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> schemas.Token:
    user = authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    token_data = {"access_token": access_token, "token_type": "bearer"}
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return token_data


@router.delete(
    "/user/{username}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user by name",
)
def delete_user_by_username(
    username: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
) -> None:
    if username != current_user.username and current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to delete this user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # if get_user_by_username(db=db, username=username) is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found",
    #     )
    delete_user(username=username, db=db)
    return None
