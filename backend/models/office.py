from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
    Column,
    ForeignKey,
    Integer)
from models.base import BaseTableID
from typing import TYPE_CHECKING, Any, List, Optional
from models.employee import EmployeeOfficeLink

if TYPE_CHECKING:
    from models.company import Company
    from models.employee import Employee



class OfficeBase(SQLModel):
    office_id: int | None = Field(default=None, alias="id", sa_column=Column(Integer, unique=True, index=True))
    name: str
    latitude: str
    longitude: str
    is_active: bool = Field(default=True)
    external_id: int | None
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
    
   
  




