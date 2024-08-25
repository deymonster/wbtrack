import redis.asyncio

from config import settings

redis_client = redis.asyncio.from_url(settings.REDIS_URL, decode_responses=True)

__all__ = [
    "redis_client",
]
