import asyncio
from http import HTTPStatus

import pytest
from freezegun import freeze_time


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


def test_auth_token_expired_after_time(client, user):
    with freeze_time('2023-07-14 12:00:00'):

        async def client_post():
            data = {'username': user.email, 'password': user.clean_password}
            return await client.post('/auth/token', data=data)

        response = asyncio.run(client_post())
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):

        async def client_put():
            json = {'username': 'wrongwrong', 'email': 'wrong@wrong.com', 'password': 'wrong'}
            headers = {'Authorization': f'Bearer {token}'}
            return await client.put(f'/users/{user.id}', headers=headers, json=json)

        response = asyncio.run(client_put())
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Token expired'}


@pytest.mark.asyncio()
async def test_auth_token_refresh_return_ok(client, user, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = await client.post('/auth/refresh_token', headers=headers)
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
    assert token['token_type'] == 'bearer'


def test_auth_token_expired_dont_refresh(client, user):
    with freeze_time('2023-07-14 12:00:00'):

        async def client_post():
            data = {'username': user.email, 'password': user.clean_password}
            return await client.post('/auth/token', data=data)

        response = asyncio.run(client_post())
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):

        async def client_post():
            headers = {'Authorization': f'Bearer {token}'}
            return await client.post('/auth/refresh_token', headers=headers)

        response = asyncio.run(client_post())
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Token expired'}
