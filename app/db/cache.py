# from typing import AsyncIterator
#
# import redis
# from opentelemetry import trace
# from opentelemetry.instrumentation.redis import RedisInstrumentor
#
# # import aioredis
# from app.utils.settings import Settings
#
# tracer = trace.get_tracer(__name__)
# settings = Settings()
# RedisInstrumentor().instrument()
#
#
# async def get_cache() -> AsyncIterator[redis.Redis]:
#     with tracer.start_as_current_span('get_cache'):
#         session = redis.ConnectionPool(
#             host=settings.REDIS_HOST,
#             port=settings.REDIS_PORT,
#             password=settings.REDIS_PASSWORD,
#             db=settings.REDIS_DB,
#             max_connections=settings.REDIS_MAX_CONNECTIONS,
#             encoding='utf-8',
#             decode_responses=True,
#         )
#         cache = redis.Redis(connection_pool=session)
#         yield cache
#         cache.close()
#
#         # cache = await aioredis.create_redis_pool(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", password=settings.REDIS_PASSWORD, encoding="utf-8", decode_responses=True)
#         # cache = await aioredis.from_url(url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", password=settings.REDIS_PASSWORD, db=settings.REDIS_DB, max_connections=settings.REDIS_MAX_CONNECTIONS, encoding="utf-8", decode_responses=True)
#         # yield cache
#         # cache.close()
#         # await cache.wait_closed()
