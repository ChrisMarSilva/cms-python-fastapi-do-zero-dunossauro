from datetime import datetime
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import User
from app.schemas import Message, Token, UserList, UserPublic, UserSchema
from app.security import create_access_token, get_current_user, get_password_hash, verify_password

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def root_read():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def users_create(request_user: UserSchema, session: Session = Depends(get_session)):
    stmt = select(User).where((User.username == request_user.username) | (User.email == request_user.email))
    db_user = session.scalar(stmt)

    if db_user:
        if db_user.username == request_user.username:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Username already exists')
        elif db_user.email == request_user.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail='Email already exists')

    hashed_password = get_password_hash(request_user.password)
    new_user = User(username=request_user.username, password=request_user.password, email=hashed_password)
    session.add(new_user)

    session.commit()
    session.refresh(new_user)

    return new_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def users_read_all(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    stmt = select(User).offset(skip).limit(limit)
    users = session.scalars(stmt).all()
    return {'users': users}


@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def users_read_one(user_id: int, session: Session = Depends(get_session)):
    stmt = select(User).where(User.id == user_id)
    db_user = session.scalar(stmt)

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return db_user


@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def users_update(user_id: int, request_user: UserSchema, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permissions')

    # stmt = select(User).where(User.id == user_id)
    # db_user = session.scalar(stmt)
    # if not db_user:
    #     raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    current_user.username = request_user.username
    current_user.password = get_password_hash(request_user.password)
    current_user.email = request_user.email
    current_user.updated_at = datetime.now()

    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def users_delete(user_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permissions')

    # stmt = select(User).where(User.id == user_id)
    # db_user = session.scalar(stmt)
    #
    # if not db_user:
    #     raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    session.delete(current_user)
    session.commit()


@app.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    stmt = select(User).where(User.email == form_data.username)
    user = session.scalar(stmt)

    if not user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect email or password')

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect email or password')

    access_token = create_access_token(data={'sub': user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}
