from http import HTTPStatus

import pytest


@pytest.mark.asyncio()
async def test_auth_token_create_return_ok(client, user, token):
    data = {'username': user.email, 'password': user.clean_password}
    response = await client.post('/auth/token', data=data)
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
    assert token['token_type'] == 'bearer'


@pytest.mark.asyncio()
async def test_auth_token_create_return_error_bad_request_email(client, user):
    data = {'username': f'err-{user.email}', 'password': user.clean_password}
    response = await client.post('/auth/token', data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


@pytest.mark.asyncio()
async def test_auth_token_create_return_error_bad_request_password(client, user):
    data = {'username': user.email, 'password': user.password}
    response = await client.post('/auth/token', data=data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


@pytest.mark.asyncio()
async def test_auth_token_refresh_return_ok(client, user, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = await client.post('/auth/refresh_token', headers=headers)
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
    assert token['token_type'] == 'bearer'
