from typing import TYPE_CHECKING, Optional
from sqlmodel import Relationship, Field, SQLModel
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from models.base import BaseTable
from models.company_user import CompanyUser
from enums.user import UserRoleEnum

from fastapi_users.db import SQLAlchemyBaseOAuthAccountTableUUID


if TYPE_CHECKING:
    from models.company import Company
    from models.employee import Employee


class UserBase(SQLModel):
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    phone: str | None
    tg_id: str | None
    role: UserRoleEnum = Field(UserRoleEnum.MANAGER, description="Role of the user")


class User(UserBase, SQLModelBaseUserDB, BaseTable, table=True):
    companies: list["Company"] = Relationship(
        back_populates="users",
        link_model=CompanyUser,
    )





