from redis.asyncio import Redis

from config import settings

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True,
    username=None,
    password=None,
    socket_connect_timeout=1,
    retry_on_timeout=True
)

__all__ = [
    "redis_client",
]
