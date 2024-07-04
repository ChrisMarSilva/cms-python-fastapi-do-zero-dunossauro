from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from app.schemas import Message, UserDB, UserList, UserPublic, UserSchema
from app.models import User

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_all_users():
    return {'users': database}


@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_one_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    return database[user_id - 1]


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(request: UserSchema):
    user_with_id = UserDB(**request.model_dump(), id=len(database) + 1)
    database.append(user_with_id)

    user = User(
        username=request.username,
        password=request.password,
        email=request.email,
    )

    return user_with_id


@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not found')

    del database[user_id - 1]

    return {'message': 'User deleted'}
