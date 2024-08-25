from uuid import UUID
from fastapi import Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from config import settings
from models.user import User


class UserService(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = settings.APP_SECRET_KEY
    verification_token_secret = settings.APP_SECRET_KEY

    async def on_after_register(
        self,
        user: User,
        request: Request | None = None,
    ):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Request | None = None,
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Request | None = None,
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
