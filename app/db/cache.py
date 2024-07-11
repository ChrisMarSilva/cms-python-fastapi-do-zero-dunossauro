from typing import AsyncIterator

from opentelemetry import trace
import redis
# import aioredis
# from redis.asyncio import Redis
# import redis.asyncio as aioredis

from app.utils.settings import Settings

tracer = trace.get_tracer(__name__)
settings = Settings()


async def get_cache() -> AsyncIterator[redis.Redis]:
    with tracer.start_as_current_span('get_cache'):
        # cache = await aioredis.create_redis_pool(f"redis://{REDIS_HOST}:{REDIS_PORT}", password=REDIS_PASSWORD, encoding="utf-8", decode_responses=True)
        # cache = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", password=REDIS_PASSWORD, encoding="utf-8", decode_responses=True)
        session = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, password=settings.REDIS_PASSWORD, db=settings.REDIS_DB, encoding="utf-8", decode_responses=True)
        cache = redis.Redis(connection_pool=session)
        yield cache
        cache.close()
        # await cache.wait_closed()
