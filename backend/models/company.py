from typing import TYPE_CHECKING

from sqlalchemy import Column
from sqlmodel import Field, Integer, Relationship, SQLModel, String

from models.base import BaseTableID
from models.company_user import CompanyUser

if TYPE_CHECKING:
    from models.office import Office
    from models.user import User


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




