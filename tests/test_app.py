from http import HTTPStatus

from app.schemas import UserPublic


def test_app_root_read_return_ok(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_app_users_create_return_created(client):
    # Arrange
    json = {'username': 'alice', 'email': 'alice@example.com', 'password': 'secret'}

    # Act
    response = client.post('/users/', json=json)

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'alice', 'email': 'alice@example.com', 'id': 1}


def test_app_users_create_return_error_bad_request_username(client, user):
    json = {'username': 'Teste', 'email': 'teste@test.com', 'password': 'secret'}
    client.post('/users/', json=json)
    response = client.post('/users/', json=json)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_app_users_create_return_error_bad_request_email(client, user):
    json = {'username': 'Teste2', 'email': 'teste@test.com', 'password': 'secret'}
    client.post('/users/', json=json)
    response = client.post('/users/', json=json)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_app_users_read_all_return_ok_empty(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_app_users_read_all_return_ok_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_app_users_read_one_return_ok(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_app_users_read_one_return_error_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_app_users_update_return_ok(client, user):
    json = {'username': 'bob', 'email': 'bob@example.com', 'password': 'mynewpassword'}
    response = client.put('/users/1', json=json)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'bob', 'email': 'bob@example.com', 'id': 1}


def test_app_users_update_return_error_not_found(client):
    json = {'username': 'bob', 'email': 'bob@example.com', 'password': 'mynewpassword'}
    response = client.put('/users/2', json=json)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_app_users_delete_return_ok(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_app_users_delete_return_error_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
