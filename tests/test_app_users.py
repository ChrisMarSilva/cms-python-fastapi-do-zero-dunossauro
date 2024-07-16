from http import HTTPStatus

import pytest

from app.schemas.user import UserResponse


@pytest.mark.asyncio()
async def test_users_read_all_return_ok_empty(client):
    response = await client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


@pytest.mark.asyncio()
async def test_users_read_all_return_ok_with_users(client, user):
    user_schema = UserResponse.model_validate(user).model_dump()
    response = await client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


@pytest.mark.asyncio()
async def test_users_read_one_return_ok(client, user, token):
    user_schema = UserResponse.model_validate(user).model_dump()
    headers = {'Authorization': f'Bearer {token}'}
    response = await client.get(f'/users/{user.id}', headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


@pytest.mark.asyncio()
async def test_users_read_one_return_error_not_forbidden(client, other_token):
    headers = {'Authorization': f'Bearer {other_token}'}
    response = await client.get('/users/999', headers=headers)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'The user do not have enough privileges'}


@pytest.mark.asyncio()
async def test_users_create_return_created(client):
    json = {'username': 'alice', 'email': 'alice@gmail.com', 'password': 'secret'}  # Arrange
    response = await client.post('/users/', json=json)  # Act
    assert response.status_code == HTTPStatus.CREATED  # Assert
    assert response.json() == {'username': 'alice', 'email': 'alice@gmail.com', 'id': 1}  # Assert


@pytest.mark.asyncio()
async def test_users_create_return_error_bad_request_username(client, user):
    json = {'username': user.username, 'email': user.email, 'password': 'secret'}
    await client.post('/users/', json=json)
    response = await client.post('/users/', json=json)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists.'}


@pytest.mark.asyncio()
async def test_users_create_return_error_bad_request_email(client, user):
    json = {'username': f'Alterado{user.username}', 'email': user.email, 'password': 'secret'}
    await client.post('/users/', json=json)
    response = await client.post('/users/', json=json)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists.'}


@pytest.mark.asyncio()
async def test_users_read_one_return_error_not_found(client, user, token):
    headers = {'Authorization': f'Bearer {token}'}

    response = await client.delete(f'/users/{user.id}', headers=headers)
    assert response.status_code == HTTPStatus.NO_CONTENT

    response = await client.get(f'/users/{user.id}', headers=headers)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


@pytest.mark.asyncio()
async def test_users_update_return_ok(client, user, token):
    json = {'username': 'bob', 'email': 'bob@example.com', 'password': 'mynewpassword'}
    headers = {'Authorization': f'Bearer {token}'}
    response = await client.put(f'/users/{user.id}', headers=headers, json=json)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'bob', 'email': 'bob@example.com', 'id': user.id}


@pytest.mark.asyncio()
async def test_users_update_return_error_forbidden(client, other_token):
    json = {'username': 'bob', 'email': 'bob@example.com', 'password': 'mynewpassword'}
    headers = {'Authorization': f'Bearer {other_token}'}
    response = await client.put('/users/999', headers=headers, json=json)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'The user do not have enough privileges'}


@pytest.mark.asyncio()
async def test_users_delete_return_ok(client, user, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = await client.delete(f'/users/{user.id}', headers=headers)
    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio()
async def test_users_delete_return_error_forbidden(client, other_token):
    headers = {'Authorization': f'Bearer {other_token}'}
    response = await client.delete('/users/999', headers=headers)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'The user do not have enough privileges'}


@pytest.mark.asyncio()
async def test_users_delete_return_error_invalid_token(client, other_token):
    invalid_token = other_token[:-1] + 'xxxxxxxxxxxxxx'
    headers = {'Authorization': f'Bearer {invalid_token}'}
    response = await client.delete('/users/999', headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
    # assert response.json() == {'detail': 'Invalid token'}


@pytest.mark.asyncio()
async def test_users_delete_return_error_token_without_sub(client):
    token_without_sub = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoiSm9obiBEb2UiLCJpYXQiOjE1MTYyMzkwMjJ9.hqWGSaFpvbrXkOWc6lrnffhNWR19W_S1YKFBx2arWBk'
    headers = {'Authorization': f'Bearer {token_without_sub}'}
    response = await client.delete('/users/999', headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
