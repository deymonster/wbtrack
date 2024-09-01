from typing import TYPE_CHECKING
from sqlmodel import Relationship, Field, SQLModel
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from models.base import BaseTable
from models.company_user import CompanyUser
from enums.user import UserRoleEnum

if TYPE_CHECKING:
    from models.company import Company


class UserBase(SQLModel):
    phone: str | None
    role: UserRoleEnum = Field(UserRoleEnum.MANAGER, description="Role of the user")


class User(UserBase, SQLModelBaseUserDB, BaseTable, table=True):
    companies: list["Company"] = Relationship(
        back_populates="users",
        link_model=CompanyUser,
    )
