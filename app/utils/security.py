from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

# from zoneinfo import ZoneInfo
from app.db.database import get_session
from app.models.user import User
from app.schemas.token import TokenData
from app.utils.settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def create_access_token(data: dict):
    to_encode = data.copy()
    # expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).astimezone(ZoneInfo("America/Sao_Paulo"))
    # expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # expire = datetime.now(tz=ZoneInfo('America/Sao_Paulo')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')

        if not username:  # pragma: no cover
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})

        token_data = TokenData(username=username)
    except DecodeError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})

    stmt = select(User).where(User.email == token_data.username)
    user = session.scalar(stmt)

    if user is None:  # pragma: no cover
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')
    # elif not user.is_active:
    #     raise HTTPException(status_code=400, detail="Inactive user")

    return user
