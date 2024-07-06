from http import HTTPStatus

import pytest
from jwt import decode

from app.utils.security import create_access_token, settings


@pytest.mark.asyncio()
async def test_security_jwt(token):
    # Arrange
    data = {'test': 'test'}
    token = create_access_token(data)

    # Act
    decoded = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    # Assert
    assert decoded['test'] == data['test']
    assert decoded['exp']


@pytest.mark.asyncio()
async def test_security_jwt_invalid_token(client):
    response = await client.delete('/users/1', headers={'Authorization': 'Bearer token-invalido'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
