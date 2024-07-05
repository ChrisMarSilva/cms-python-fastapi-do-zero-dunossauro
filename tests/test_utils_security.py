from http import HTTPStatus

from jwt import decode

from app.utils.security import create_access_token, settings


def test_security_jwt():
    # Arrange
    data = {'test': 'test'}
    token = create_access_token(data)

    # Act
    decoded = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    # Assert
    assert decoded['test'] == data['test']
    assert decoded['exp']


def test_security_jwt_invalid_token(client):
    response = client.delete('/users/1', headers={'Authorization': 'Bearer token-invalido'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
