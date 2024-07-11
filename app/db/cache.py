from typing import AsyncIterator

from opentelemetry import trace
import redis
# import aioredis
# from redis.asyncio import Redis
# import redis.asyncio as aioredis

tracer = trace.get_tracer(__name__)
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = '123'
REDIS_DB = 0
REDIS_MAX_CONNECTIONS = 100


async def get_cache() -> AsyncIterator[redis.Redis]:
    with tracer.start_as_current_span('get_cache'):
        # cache = await aioredis.create_redis_pool(f"redis://{REDIS_HOST}:{REDIS_PORT}", password=REDIS_PASSWORD, encoding="utf-8", decode_responses=True)
        # cache = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", password=REDIS_PASSWORD, encoding="utf-8", decode_responses=True)
        session = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB, encoding="utf-8", decode_responses=True)
        cache = redis.Redis(connection_pool=session)
        yield cache
        cache.close()
        # await cache.wait_closed()
