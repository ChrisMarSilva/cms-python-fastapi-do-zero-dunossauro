from http import HTTPStatus

import pytest


@pytest.mark.asyncio()
async def test_app_root_read_return_ok(client):
    response = await client.get('/root')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}
