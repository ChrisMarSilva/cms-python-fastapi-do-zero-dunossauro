from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

# from zoneinfo import ZoneInfo
from app.database import get_session
from app.models import User
from app.schemas import TokenData

SECRET_KEY = 'lv2srm*0^k(kbcq_o2nv&feiku@ot2qn0ykmm8ab==*88+yp@p'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def create_access_token(data: dict):
    to_encode = data.copy()
    # expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES).astimezone(ZoneInfo("America/Sao_Paulo"))
    # expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # expire = datetime.now(tz=ZoneInfo('America/Sao_Paulo')) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')

        if not username:  # pragma: no cover
            raise credentials_exception

        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception

    stmt = select(User).where(User.email == token_data.username)
    user = session.scalar(stmt)

    if user is None:  # pragma: no cover
        raise credentials_exception

    return user
