import json
from datetime import datetime
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
import redis

from app.db.cache import get_cache
from app.db.database import get_session
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserRequest, UserResponse, UsersResponse
from app.utils.security import get_current_user, get_password_hash
from app.utils.tracing import instrument_async

router = APIRouter()
T_CurrentUserDep = Annotated[User, Depends(get_current_user)]
T_SessionDep = Annotated[AsyncSession, Depends(get_session)]
T_CacheDep = Annotated[redis.Redis, Depends(get_cache)]


@instrument_async('calling users_create')
@router.post(path='/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def users_create(request: UserRequest, session: T_SessionDep, cache: T_CacheDep):
    if cache.exists(f"users_username_{request.username}"):
        return JSONResponse(content={'detail': 'Username already exists(cache).'}, status_code=HTTPStatus.CONFLICT)
    if cache.exists(f"users_email_{request.email}"):
        return JSONResponse(content={'detail': 'Email already exists(cache).'}, status_code=HTTPStatus.CONFLICT)

    db_user = await UserRepository.get_by_username_or_email(session, request.username, request.email)
    if db_user:
        cache.delete(f"users_all")
        cache.delete(f"users_skip")
        cache.delete(f"users_limit")
        cache.set(f"users_username_{db_user.username}", db_user.as_json())
        cache.set(f"users_email_{db_user.email}", db_user.as_json())
        if db_user.username == request.username:
            return JSONResponse(content={'detail': 'Username already exists(db).'}, status_code=HTTPStatus.CONFLICT)
        elif db_user.email == request.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Email already exists(db).')

    db_user = User(username=request.username, password=get_password_hash(request.password), email=request.email)
    db_user = await UserRepository.create(session=session, user=db_user)
    # try:
    # except errors.DuplicateKeyError:
    #     return JSONResponse(content={"detail": f"Username already exists"}, status_code=HTTPStatus.CONFLICT)

    json_user = db_user.as_json()
    cache.set(f"users_username_{db_user.username}", json_user)
    cache.set(f"users_email_{db_user.email}", json_user)
    cache.delete(f"users_all")
    cache.delete(f"users_skip")
    cache.delete(f"users_limit")

    return db_user


@instrument_async('calling users_read_all')
@router.get(path='/', response_model=UsersResponse, status_code=HTTPStatus.OK)
async def users_read_all(session: T_SessionDep, cache: T_CacheDep, skip: int = 0, limit: int = 100):
    users_skip = cache.get("users_skip")
    users_limit = cache.get("users_limit")
    if users_skip and users_limit:
        if int(users_skip) != skip or int(users_limit) != limit:
            cache.delete(f"users_skip")
            cache.delete(f"users_limit")
            cache.delete(f"users_all")

    users_cache = cache.get("users_all")
    if users_cache:
        users_cache = json.loads(users_cache)
        users_cache = [json.loads(u) for u in users_cache]
        return UsersResponse(users=users_cache)

    users_db = await UserRepository.get_all(session=session, skip=skip, limit=limit)
    if users_db:
        users_json = [user.as_json() for user in users_db]
        cache.set("users_all", json.dumps(users_json))
        cache.set("users_skip", skip)
        cache.set("users_limit", limit)

    return UsersResponse(users=users_db)


@instrument_async('calling users_read_one')
@router.get(path='/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
async def users_read_one(user_id: int, current_user: T_CurrentUserDep):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='The user do not have enough privileges')

    return current_user


@instrument_async('calling users_update')
@router.put(path='/{user_id}', response_model=UserResponse, status_code=HTTPStatus.OK)
async def users_update(user_id: int, request: UserRequest, session: T_SessionDep, cache: T_CacheDep, current_user: T_CurrentUserDep) -> User:
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='The user do not have enough privileges')

    current_user.username = request.username
    current_user.password = get_password_hash(request.password)
    current_user.email = request.email
    current_user.updated_at = datetime.now()

    current_user = await UserRepository.update(session=session, user=current_user)

    json_user = current_user.as_json()
    cache.set(f"users_username_{current_user.username}", json_user)
    cache.set(f"users_email_{current_user.email}", json_user)
    cache.delete(f"users_all")
    cache.delete(f"users_skip")
    cache.delete(f"users_limit")

    return current_user


@instrument_async('calling delete_user')
@router.delete(path='/{user_id}', status_code=HTTPStatus.NO_CONTENT)
async def delete_user(user_id: int, session: T_SessionDep, cache: T_CacheDep, current_user: T_CurrentUserDep):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='The user do not have enough privileges')

    cache.delete(f"users_username_{current_user.username}")
    cache.delete(f"users_email_{current_user.email}")
    cache.delete(f"users_all")
    cache.delete(f"users_skip")
    cache.delete(f"users_limit")

    await UserRepository.delete(session=session, user=current_user)
