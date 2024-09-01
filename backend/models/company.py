from typing import TYPE_CHECKING
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ENUM, ARRAY
from sqlmodel import Field, Relationship, SQLModel

from models.base import BaseTableID
from models.company_user import CompanyUser

if TYPE_CHECKING:
    from models.user import User
    from models.office import Office


class CompanyBase(SQLModel):
    name: str
    phone: str


class Company(CompanyBase, BaseTableID, table=True):

    users: list["User"] = Relationship(
        back_populates="companies",
        link_model=CompanyUser,
    )
    offices: list["Office"] = Relationship(
        back_populates="company",
    )

