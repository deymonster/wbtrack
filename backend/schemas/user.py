from typing import Optional

from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import BaseModel, EmailStr

from enums.user import UserRoleEnum


class IUserRead(BaseUser):
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    phone: str | None
    role: UserRoleEnum


class IUserCreate(BaseUserCreate):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    phone: str | None = None
    tg_id: str | None = None



class IUserUpdate(BaseUserUpdate):
    pass


class RefreshTokenRequest(BaseModel):
    refresh_token: str
    is_employer: bool = False


class RegisterResponse(BaseModel):
    registration_link: str