from typing import TYPE_CHECKING
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ENUM, ARRAY
from sqlmodel import Field, Relationship, SQLModel, String, Integer

from models.base import BaseTableID
from models.company_user import CompanyUser

if TYPE_CHECKING:
    from models.user import User
    from models.office import Office
    from models.employee import Employee


class CompanyBase(SQLModel):
    wb_user_id: int | None = Field(
        sa_column=Column(Integer, unique=True, index=True)
    )
    name: str | None = None
    phone: str = Field(sa_column=Column(String, unique=True, index=True))
    org_name: str | None = None


class Company(CompanyBase, BaseTableID, table=True):

    users: list["User"] = Relationship(
        back_populates="companies",
        link_model=CompanyUser,
    )
    offices: list["Office"] = Relationship(
        back_populates="company",
    )
 



