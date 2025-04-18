from typing import TYPE_CHECKING

from sqlmodel import Column, Field, ForeignKey, Integer, Relationship, SQLModel

from models.base import BaseTableID
from models.employee import EmployeeOfficeLink

if TYPE_CHECKING:
    from models.company import Company
    from models.employee import Employee
    from models.office_expenses import OfficeExpenses
    from models.office_report import OfficeReport


class OfficeBase(SQLModel):
    office_id: int | None = Field(default=None, alias="id", sa_column=Column(Integer, unique=True, index=True))
    name: str
    latitude: str
    longitude: str
    is_active: bool = Field(default=True)
    external_id: int = Field(unique=True, index=True)
    rate: float | None = Field(default=0.0)


class Office(OfficeBase, BaseTableID, table=True):
    company_id: int | None = Field(
        sa_column=Column(
            Integer,
            ForeignKey("company.id", ondelete="CASCADE"),
        ),
        default=None,
    )
    company: "Company" = Relationship(back_populates="offices")
    employees: list["Employee"] = Relationship(
        back_populates="offices",
        link_model=EmployeeOfficeLink
    )
    expenses: "OfficeExpenses" = Relationship(back_populates="office")
    reports: list["OfficeReport"] = Relationship(back_populates="office")







