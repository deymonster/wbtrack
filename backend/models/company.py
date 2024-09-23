from typing import TYPE_CHECKING
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ENUM, ARRAY
from sqlmodel import Field, Relationship, SQLModel

from models.base import BaseTableID
from models.company_user import CompanyUser

if TYPE_CHECKING:
    from models.user import User
    from models.office import Office
    from models.employee import Employee


class CompanyBase(SQLModel):
    supplier_id: int | None = None
    name: str | None = None
    phone: str = Field(unique=True, index=True)


class Company(CompanyBase, BaseTableID, table=True):

    users: list["User"] = Relationship(
        back_populates="companies",
        link_model=CompanyUser,
    )
    offices: list["Office"] = Relationship(
        back_populates="company",
    )
    employees: list["Employee"] = Relationship(
        back_populates="company"
    )



