from uuid import UUID
from fastapi import Depends
import jwt
from fastapi_async_sqlalchemy import db
from fastapi_users import FastAPIUsers, models
from fastapi_users.jwt import generate_jwt
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from core.redis import redis_client
from models.employee import Employee
from models.user import User
from services.user import UserService
from config import settings

access_bearer_transport = BearerTransport(
    tokenUrl="api/v1/auth/login",
)

refresh_bearer_transport = BearerTransport(tokenUrl="auth/v1/refresh-token")

#
# class RefreshJWTStrategy(JWTStrategy):
#     """Custom JWT Strategy for refresh token"""
#     def __init__(self,  secret: str, lifetime_seconds: int, algorithm: str = "HS256"):
#         super().__init__(secret=secret, lifetime_seconds=lifetime_seconds, algorithm=algorithm)
#         self.secret = secret
#         self.lifetime_seconds = lifetime_seconds
#         self.algorithm = algorithm
#
#     async def write_token(self, user_id: str) -> str:
#         payload = {"sub": user_id}
#         return generate_jwt(
#             data=payload,
#             secret=self.secret,
#             lifetime_seconds=self.lifetime_seconds,
#             algorithm=self.algorithm
#         )
#
#     async def read_token(self, token: str):
#         try:
#             payload = jwt.decode(
#                 token,
#                 self.secret,
#                 algorithms=[self.algorithm],
#             )


def create_employee_jwt_access(employee: Employee) -> str:
    payload = {
        "sub": employee.id,
        "aud": "employee",
        "employee_id": employee.employee_id,
        "first_name": employee.first_name,
        "middle_name": employee.middle_name,
        "last_name": employee.last_name,
        "tg_id": employee.tg_id
    }
    access_token = generate_jwt(
        data=payload,
        secret=settings.APP_SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME,
        algorithm="HS256"
    )
    return access_token


def create_employee_jwt_refresh(employee: Employee) -> str:
    payload = {
        "sub": employee.id,
        "aud": "employee"
    }
    refresh_token = generate_jwt(
        data=payload,
        secret=settings.APP_SECRET_KEY,
        lifetime_seconds=settings.REFRESH_TOKEN_LIFETIME,
        algorithm="HS256"
    )
    return refresh_token


def get_access_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.APP_SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_LIFETIME)  # one hour for access token


def get_refresh_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.APP_SECRET_KEY,
        lifetime_seconds=settings.REFRESH_TOKEN_LIFETIME)  # one week for refresh token


access_backend = AuthenticationBackend(
    name="access",
    transport=access_bearer_transport,
    get_strategy=get_access_strategy,
)

refresh_backend = AuthenticationBackend(
    name="refresh",
    transport=refresh_bearer_transport,
    get_strategy=get_refresh_strategy,
)


async def get_user_session():
    yield SQLAlchemyUserDatabase(db.session, User)


async def get_user_service(
    user_session: SQLAlchemyUserDatabase = Depends(get_user_session),
):
    yield UserService(user_session)


fastapi_users = FastAPIUsers[User, UUID](get_user_service, [access_backend, refresh_backend])

__all__ = [
    "fastapi_users",
    "access_backend",
    "refresh_backend",
    "create_employee_jwt_access",
    "create_employee_jwt_refresh"
]
