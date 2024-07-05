from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.repositories.user import UserRepository
from app.utils.settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()
SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='auth/token'))]


def create_access_token(data: dict):
    to_encode = data.copy()
    # expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).astimezone(ZoneInfo("America/Sao_Paulo"))
    # expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # expire = datetime.now(tz=ZoneInfo('America/Sao_Paulo')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # dt = datetime.datetime.now(timezone.utc)
    # dt.replace(tzinfo=timezone.utc)
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(session: SessionDep, token: TokenDep):
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except DecodeError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})

    email: str = payload.get('sub')
    if not email:  # pragma: no cover
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})

    user = UserRepository.get_by_email(session=session, email=email)
    if user is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return user
