import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api import app
from app.db.database import get_session
from app.models import table_registry
from app.models.user import User
from app.utils.security import get_password_hash


@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture()
def user(session):
    user = User(username='Teste', email='teste@test.com', password=get_password_hash('testtest'))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest'

    return user


@pytest.fixture()
def user2(session):
    user = User(username='Teste2', email='teste2@test.com', password=get_password_hash('testtest2'))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = 'testtest2'

    return user


@pytest.fixture()
def token(client, user):
    response = client.post('/auth/token', data={'username': user.email, 'password': user.clean_password})
    return response.json()['access_token']


@pytest.fixture()
def token2(client, user2):
    response = client.post('/auth/token', data={'username': user2.email, 'password': user2.clean_password})
    return response.json()['access_token']
