from redis import asyncio as aioredis
from settings import Settings


settings = Settings()


def get_redis_connection() -> aioredis.Redis:
    return aioredis.Redis(
        host=settings.CACHE_HOST, port=settings.CACHE_PORT, db=settings.CACHE_DB
    )
