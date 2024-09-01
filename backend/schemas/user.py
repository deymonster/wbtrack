from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import BaseModel, EmailStr

class IUserRead(BaseUser):
    pass


class IUserCreate(BaseUserCreate):
    phone: str | None = None


class IUserUpdate(BaseUserUpdate):
    pass