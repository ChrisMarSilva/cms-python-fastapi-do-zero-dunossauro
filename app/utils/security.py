import json
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, InvalidTokenError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession
import redis
from opentelemetry import trace

from app.db.cache import get_cache
from app.db.database import get_session
from app.models.user import User
from app.repositories.user import UserRepository
from app.utils.settings import Settings
from app.utils.tracing import instrument

settings = Settings()
pwd_context = PasswordHash.recommended()
T_TokenDep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='auth/token'))]
T_SessionDep = Annotated[AsyncSession, Depends(get_session)]
T_CacheDep = Annotated[redis.Redis, Depends(get_cache)]
tracer = trace.get_tracer(__name__)

@instrument('calling create_access_token')
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@instrument('calling get_password_hash')
def get_password_hash(password: str):
    return pwd_context.hash(password)


@instrument('calling verify_password')
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(session: T_SessionDep, cache: T_CacheDep, token: T_TokenDep) -> User:
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except DecodeError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})
    except ExpiredSignatureError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Token expired', headers={'WWW-Authenticate': 'Bearer'})
    except InvalidTokenError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid token', headers={'WWW-Authenticate': 'Bearer'})

    email: str = payload.get('sub')
    if not email:  # pragma: no cover
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})

    # try:
    # except ValueError as exc:
    # span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
    # except ValueError as exc:
    # span.record_exception(exc)
    # span.set_status(trace.Status(trace.StatusCode.ERROR, str(exc)))
    # except Exception as ex:
    # span.record_exception(ex)
    # span.set_status(Status(StatusCode.ERROR))
    #
    # if span.is_recording():
    # span.set_attribute("enduser.id", kwargs["id"])
    # span.set_attribute("enduser.email", kwargs["email"])

    with tracer.start_as_current_span('get by cache') as span:
        span.add_event("get email")
        cache_user = cache.get(f"users_email_{email}")
        if cache_user:
            span.add_event("found")
            return User(**json.loads(cache_user))
        span.add_event("not found")

    with tracer.start_as_current_span('get by db') as span:
        span.add_event("get email")
        db_user = await UserRepository.get_by_email(session=session, email=email)
        if db_user is None:
            span.add_event("not found")
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
        span.add_event("found")

    with tracer.start_as_current_span('set by cache') as span:
        span.add_event("delete")
        cache.delete(f"users_all")
        cache.delete(f"users_skip")
        cache.delete(f"users_limit")

        span.add_event("set")
        json_user = db_user.as_json()
        cache.set(f"users_username_{db_user.username}", json_user)
        cache.set(f"users_email_{db_user.email}", json_user)

    return db_user
