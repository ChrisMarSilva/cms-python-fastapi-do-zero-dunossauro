from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    # Arrange
    # from fastapi.testclient import TestClient
    # from app.main import app
    # client = TestClient(app)
    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user_deve_retornar_created(client):
    json = {'username': 'alice', 'email': 'alice@example.com', 'password': 'secret'}
    response = client.post('/users/', json=json)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {'username': 'alice', 'email': 'alice@example.com', 'id': 1}


def test_read_users_deve_retornar_ok(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [{'username': 'alice', 'email': 'alice@example.com', 'id': 1}]}


def test_read_users_1_deve_retornar_ok(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'alice', 'email': 'alice@example.com', 'id': 1}


def test_read_users_1_deve_retornar_erro_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user_deve_retornar_ok(client):
    json = {'username': 'bob', 'email': 'bob@example.com', 'password': 'mynewpassword'}
    response = client.put('/users/1', json=json)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'bob', 'email': 'bob@example.com', 'id': 1}


def test_update_user_deve_retornar_erro_not_found(client):
    json = {'username': 'bob', 'email': 'bob@example.com', 'password': 'mynewpassword'}
    response = client.put('/users/2', json=json)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user_deve_retornar_ok(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_deve_retornar_erro_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
