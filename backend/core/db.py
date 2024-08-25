import json
from typing import Any

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings


def pydantic_serializer(value):
    json_method = getattr(value, "model_dump_json", None)
    if callable(json_method):
        return value.model_dump_json()
    if isinstance(value, dict):
        return json.dumps(value)
    if isinstance(value, list):
        return json.dumps(value)
    return value


POOL_SIZE = max(settings.POSTGRES_POOL_SIZE // settings.WEB_CONCURRENCY, 5)

connect_args = {"check_same_thread": False}


def get_db_session(poolclass=NullPool):
    config: dict[str, Any] = {}

    if poolclass is not NullPool:
        config["pool_size"] = POOL_SIZE
        config["max_overflow"] = settings.POSTGRES_MAX_OVERFLOW
    else:
        config["poolclass"] = poolclass

    async_engine = create_async_engine(
        str(settings.DB_ASYNC_CONNECTION_STR),
        echo=False,
        future=True,
        json_serializer=pydantic_serializer,
        **config,
    )

    return async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
