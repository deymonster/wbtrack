from uuid import UUID
from fastapi import Depends
from fastapi_async_sqlalchemy import db
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    RedisStrategy,
    AuthenticationBackend,
    BearerTransport,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from core.redis import redis_client
from models.user import User
from services.user import UserService

bearer_transport = BearerTransport(
    tokenUrl="api/v1/auth/login",
)

auth_backend = AuthenticationBackend(
    name="redis",
    transport=bearer_transport,
    get_strategy=lambda: RedisStrategy(redis_client, lifetime_seconds=3600),
)


async def get_user_session():
    yield SQLAlchemyUserDatabase(db.session, User)


async def get_user_service(
    user_session: SQLAlchemyUserDatabase = Depends(get_user_session),
):
    yield UserService(user_session)


fastapi_users = FastAPIUsers[User, UUID](get_user_service, [auth_backend])

__all__ = [
    "fastapi_users",
    "auth_backend",
]
