from http import HTTPStatus


def setup_function(): ...


def test_app_root_read_return_ok(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}
