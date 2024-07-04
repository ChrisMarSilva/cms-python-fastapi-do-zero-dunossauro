from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.models.user import User
from app.schemas.user import UserList, UserPublic, UserSchema
from app.utils.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def users_create(request_user: UserSchema, session: Session):
    stmt = select(User).where((User.username == request_user.username) | (User.email == request_user.email))
    db_user = session.scalar(stmt)

    if db_user:
        if db_user.username == request_user.username:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Username already exists')
        elif db_user.email == request_user.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Email already exists')

    hashed_password = get_password_hash(request_user.password)
    db_user = User(username=request_user.username, password=hashed_password, email=request_user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def users_read_all(session: Session, skip: int = 0, limit: int = 100):
    stmt = select(User).offset(skip).limit(limit)
    users = session.scalars(stmt).all()
    return {'users': users}


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def users_read_one(user_id: int, session: Session):
    stmt = select(User).where(User.id == user_id)
    db_user = session.scalar(stmt)

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return db_user


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def users_update(user_id: int, user: UserSchema, session: Session, current_user: CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email
    current_user.updated_at = datetime.now()
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, session: Session, current_user: CurrentUser):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    session.delete(current_user)
    session.commit()
