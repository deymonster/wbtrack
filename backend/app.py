from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from fastapi_cache import FastAPICache
from fastapi_pagination import add_pagination
from api.router import api_router
from config import settings
from core.db import pydantic_serializer
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


def create_app():
    app = FastAPI(
        title="WB-Track",
        version="0.1",
        openapi_url="/openapi.json" if settings.DEBUG else None,
        docs_url="/docs" if settings.DEBUG else None,
        debug=settings.DEBUG,
        lifespan=lifespan,
        middleware=[
            Middleware(
                SQLAlchemyMiddleware,
                db_url=settings.DB_ASYNC_CONNECTION_STR,
                engine_args=dict(
                    echo=settings.DEBUG,
                    pool_pre_ping=True,
                    pool_size=settings.POSTGRES_POOL_SIZE_BY_SERVER,
                    max_overflow=settings.POSTGRES_MAX_OVERFLOW,
                    json_serializer=pydantic_serializer,
                ),
                session_args=dict(
                    autoflush=False,
                    autocommit=False,
                ),
            ),
            Middleware(
                SessionMiddleware,
                secret_key=settings.APP_SECRET_KEY,
            ),
            Middleware(
                CORSMiddleware,
                allow_origins=settings.ALLOW_ORIGINS,
                allow_origin_regex=settings.ALLOW_ORIGIN_REGEX,
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            ),
        ],
    )

    app.include_router(api_router)

    # create_admin_panel(app)

    add_pagination(app)

    return app
