from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_session
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserRequest, UserResponse, UsersResponse
from app.utils.security import get_current_user, get_password_hash

router = APIRouter()
T_SessionDep = Annotated[AsyncSession, Depends(get_session)]
T_CurrentUserDep = Annotated[User, Depends(get_current_user)]


@router.post(path='/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def users_create(request: UserRequest, session: T_SessionDep):
    db_user = await UserRepository.get_by_username_or_email(session, request.username, request.email)
    if db_user:
        if db_user.username == request.username:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Username already exists')
        elif db_user.email == request.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Email already exists')

    db_user = User(username=request.username, password=get_password_hash(request.password), email=request.email)
    db_user = await UserRepository.create(session=session, user=db_user)

    return db_user


@router.get(path='/', response_model=UsersResponse, status_code=HTTPStatus.OK)
async def users_read_all(session: T_SessionDep, skip: int = 0, limit: int = 100):
    users = await UserRepository.get_all(session=session, skip=skip, limit=limit)

    return UsersResponse(users=users)  # {'users': users}


@router.get(path='/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
async def users_read_one(user_id: int, current_user: T_CurrentUserDep):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='The user do not have enough privileges')

    return current_user


@router.put(path='/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
async def users_update(user_id: int, request: UserRequest, session: T_SessionDep, current_user: T_CurrentUserDep) -> User:
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='The user do not have enough privileges')

    current_user.username = request.username
    current_user.password = get_password_hash(request.password)
    current_user.email = request.email
    current_user.updated_at = datetime.now()

    current_user = await UserRepository.update(session=session, user=current_user)

    return current_user


@router.delete(path='/{user_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int, session: T_SessionDep, current_user: T_CurrentUserDep):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='The user do not have enough privileges')

    await UserRepository.delete(session=session, user=current_user)
