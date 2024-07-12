import pytest

# import redis
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from app.api import app
from app.db.database import get_session
from app.models import table_registry
from app.models.user import User
from app.repositories.user import UserRepository
from app.utils.security import get_password_hash


@pytest.fixture()
async def client(session: AsyncSession) -> AsyncClient:
    async def get_session_override():
        return session

    try:
        async with AsyncClient(app=app, base_url='http://test') as client:
            app.dependency_overrides[get_session] = get_session_override
            yield client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture()
async def session() -> AsyncSession:
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    try:
        async with engine.begin() as conn:
            # await conn.run_sync(table_registry.metadata.drop_all)
            await conn.run_sync(table_registry.metadata.create_all)

        async with AsyncSession(engine) as session:
            yield session

        async with engine.begin() as conn:
            await conn.run_sync(table_registry.metadata.drop_all)
    finally:
        await engine.dispose()


# @pytest.fixture(autouse=True)
# async def cache() -> redis.asyncio.Redis:
#     session = redis.ConnectionPool(
#         host='localhost',
#         port=6379,
#         password='123',
#         db=0,
#         max_connections=100,
#         encoding='utf-8',
#         decode_responses=True,
#     )
#     cache = redis.Redis(connection_pool=session)
#     yield cache
#     cache.close()


@pytest.fixture()
async def user(session: AsyncSession) -> User:
    user = User(username='Teste', email='teste@test.com', password=get_password_hash('testtest'))
    user = await UserRepository.create(session=session, user=user)
    user.clean_password = 'testtest'  # hack monkey-patch
    return user


@pytest.fixture()
async def other_user(session: AsyncSession) -> User:
    user = User(username='Teste2', email='teste2@test.com', password=get_password_hash('testtest2'))
    user = await UserRepository.create(session=session, user=user)
    user.clean_password = 'testtest2'  # hack monkey-patch
    return user


@pytest.fixture()
async def token(client: AsyncClient, user: User) -> str:
    response = await client.post('/auth/token', data={'username': user.email, 'password': user.clean_password})
    return response.json()['access_token']


@pytest.fixture()
async def other_token(client: AsyncClient, other_user: User) -> str:
    response = await client.post('/auth/token', data={'username': other_user.email, 'password': other_user.clean_password})
    return response.json()['access_token']
