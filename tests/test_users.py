from http import HTTPStatus

from app.schemas.user import UserPublic


def test_users_create_return_created(client):
    json = {'username': 'alice', 'email': 'alice@gmail.com', 'password': 'secret'}  # Arrange
    response = client.post('/users/', json=json)  # Act
    assert response.status_code == HTTPStatus.CREATED  # Assert
    assert response.json() == {'username': 'alice', 'email': 'alice@gmail.com', 'id': 1}  # Assert


def test_users_create_return_error_bad_request_username(client, user):
    json = {'username': 'Teste', 'email': 'teste@test.com', 'password': 'secret'}
    client.post('/users/', json=json)
    response = client.post('/users/', json=json)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_users_create_return_error_bad_request_email(client, user):
    json = {'username': 'Teste2', 'email': 'teste@test.com', 'password': 'secret'}
    client.post('/users/', json=json)
    response = client.post('/users/', json=json)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_users_read_all_return_ok_empty(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_users_read_all_return_ok_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_users_read_one_return_ok(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_users_read_one_return_error_not_found(client):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_users_update_return_ok(client, user, token):
    json = {'username': 'bob', 'email': 'bob@example.com', 'password': 'mynewpassword'}
    headers = {'Authorization': f'Bearer {token}'}
    response = client.put(f'/users/{user.id}', headers=headers, json=json)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'bob', 'email': 'bob@example.com', 'id': user.id}


def test_users_update_return_error_not_found(client, user, token2):
    json = {'username': 'bob', 'email': 'bob@example.com', 'password': 'mynewpassword'}
    headers = {'Authorization': f'Bearer {token2}'}
    response = client.put(f'/users/{user.id}', headers=headers, json=json)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_users_delete_return_ok(client, user, token):
    headers = {'Authorization': f'Bearer {token}'}
    response = client.delete(f'/users/{user.id}', headers=headers)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_users_delete_return_error_not_found(client, user, token2):
    headers = {'Authorization': f'Bearer {token2}'}
    response = client.delete(f'/users/{user.id}', headers=headers)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
