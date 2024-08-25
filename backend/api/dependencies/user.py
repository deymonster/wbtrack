from core.user_management import fastapi_users

current_active_user = fastapi_users.current_user(active=True)

__all__ = [
    "current_active_user",
]
