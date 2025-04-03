from fastapi import Depends, HTTPException

from core.user_management import fastapi_users
from enums.user import UserRoleEnum
from models.user import User

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

current_active_user_dependency = Depends(current_active_user)

async def current_admin_user(user: User = current_active_user_dependency) -> User:
    if user.role != UserRoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Admin role required")
    if not user.is_subscription_active:
        raise HTTPException(status_code=403, detail="Active subscription required")
    return user

__all__ = [
    "current_active_user",
    "current_admin_user",
    "current_superuser",
]
