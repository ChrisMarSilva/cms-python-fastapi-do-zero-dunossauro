from http import HTTPStatus


def test_auth_token_create_return_created(client, user):
    response = client.post('/auth/token', data={'username': user.email, 'password': user.clean_password})
    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_auth_token_create_return_error_bad_request_email(client, user):
    response = client.post('/auth/token', data={'username': f'err-{user.email}', 'password': user.clean_password})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_auth_token_create_return_error_bad_request_password(client, user):
    response = client.post('/auth/token', data={'username': user.email, 'password': user.password})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}
