from fastapi import APIRouter

from core.user_management import fastapi_users
from schemas.user import IUserRead, IUserUpdate


router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(IUserRead, IUserUpdate),
)

