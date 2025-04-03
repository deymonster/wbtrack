from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Column, Field, Relationship, SQLModel, String

from models.base import BaseTableID


class EmployeeOfficeLink(SQLModel, table=True):
    employee_id: int = Field(foreign_key="employee.id", primary_key=True)
    office_id: int = Field(foreign_key="office.id", primary_key=True)


if TYPE_CHECKING:
    from models.office import Office


class EmployeeBase(SQLModel):
    create_date: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(unique=True, index=True)
    name: str
    last_name: str
    is_deleted: bool
    phone: str = Field(sa_column=Column(String, unique=True, index=True))
    tg_id: int | None = Field(default=None)


class Employee(EmployeeBase, BaseTableID, table=True):

    offices: list["Office"] = Relationship(
        back_populates="employees",
        link_model=EmployeeOfficeLink
    )





