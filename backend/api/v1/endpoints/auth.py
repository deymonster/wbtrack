from fastapi import APIRouter

from core.user_management import auth_backend, fastapi_users
from schemas.user import IUserCreate, IUserRead


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)

router.include_router(
    fastapi_users.get_register_router(IUserRead, IUserCreate),
)

router.include_router(
    fastapi_users.get_reset_password_router(),
)

router.include_router(
    fastapi_users.get_verify_router(IUserRead),
)
