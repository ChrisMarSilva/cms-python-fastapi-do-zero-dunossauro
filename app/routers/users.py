from datetime import datetime
from http import HTTPStatus
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.models.user import User
from app.schemas.user import UserRequest, UserResponse, UsersResponse
from app.utils.security import get_current_user, get_password_hash

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def users_create(request_user: UserRequest, session: SessionDep) -> Any:
    """
    Create new user.
    """

    # curso = CursoRepository.save(db, Curso(**request.dict()))
    # return CursoResponse.from_orm(curso)
    # from uuid import uuid4
    #  id=uuid4(),
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


@router.get('/', response_model=UsersResponse, status_code=HTTPStatus.OK)
async def users_read_all(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """

    # cursos = CursoRepository.find_all(db)
    # return [CursoResponse.from_orm(curso) for curso in cursos]
    stmt = select(User).offset(skip).limit(limit)
    users = session.scalars(stmt).all()
    return {'users': users}


@router.get('/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
async def users_read_one(user_id: int, current_user: CurrentUserDep) -> Any:
    """
    Get a specific user by id.
    """

    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='The user do not have enough privileges')

    # curso = CursoRepository.find_by_id(db, id)
    # return CursoResponse.from_orm(curso)
    # stmt = select(User).where(User.id == user_id)
    # db_user = session.scalar(stmt)  # session.get(User, user_id)
    # if not db_user:
    #     raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return current_user


@router.put('/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
async def users_update(user_id: int, request_user: UserRequest, session: SessionDep, current_user: CurrentUserDep) -> Any:
    """
    Update own user.
    """

    # if not CursoRepository.exists_by_id(db, id):
    # curso = CursoRepository.save(db, Curso(id=id, **request.dict()))
    # return CursoResponse.from_orm(curso)
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='The user do not have enough privileges')

    # user_data = request_user.model_dump(exclude_unset=True)
    # current_user.sqlmodel_update(user_data)
    # session.add(current_user)

    current_user.username = request_user.username
    current_user.password = get_password_hash(request_user.password)
    current_user.email = request_user.email
    current_user.updated_at = datetime.now()
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int, session: SessionDep, current_user: CurrentUserDep):
    """
    Delete own user.
    """

    # if not CursoRepository.exists_by_id(db, id):
    # CursoRepository.delete_by_id(db, id)
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='The user do not have enough privileges')

    session.delete(current_user)
    session.commit()
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
