from fastapi import Depends, HTTPException
from core.user_management import fastapi_users
from models.user import User
from enums.user import UserRoleEnum

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

async def current_admin_user(user: User = Depends(current_active_user)) -> User:
    if user.role != UserRoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Admin role required")
    if not user.is_subscription_active:
        raise HTTPException(status_code=403, detail="Active subscription required")
    return user

__all__ = [
    "current_active_user",
    "current_superuser",
    "current_admin_user",
]
