from datetime import datetime

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import BaseModel

from enums.user import UserRoleEnum


class IUserRead(BaseUser):
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    phone: str | None
    role: UserRoleEnum
    is_subscription_active: bool
    subscription_start_date: datetime | None
    subscription_end_date: datetime | None
    created_at: datetime
    created_by_id: str | None
    parent_admin_id: str | None


class IUserCreate(BaseUserCreate):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    phone: str | None = None
    tg_id: str | None = None


class IUserUpdate(BaseUserUpdate):
    pass


class UserResponse(IUserRead):
    pass


class RefreshTokenRequest(BaseModel):
    refresh_token: str
    is_employer: bool = False


class RegisterResponse(BaseModel):
    registration_link: str
