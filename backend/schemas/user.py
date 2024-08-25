from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate


class IUserRead(BaseUser):
    pass


class IUserCreate(BaseUserCreate):
    pass


class IUserUpdate(BaseUserUpdate):
    pass