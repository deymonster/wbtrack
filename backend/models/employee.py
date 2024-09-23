from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
    Column,
    ForeignKey,
    Integer,
    ARRAY,
    String
)
from models.base import BaseTableID
from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from models.company import Company
    from models.user import User


class EmployeeBase(SQLModel):
    create_date: str
    employee_id: int = Field(unique=True, index=True)
    first_name: str
    is_deleted: bool
    last_name: str
    middle_name: str
    phones: List[str] = Field(sa_column=Column(ARRAY(String)))
    rating: float | None = None
    shortages_sum: float | None = None
    tg_id: int | None


class Employee(EmployeeBase, BaseTableID, table=True):
    company_id: int | None = Field(
        sa_column=Column(
            Integer,
            ForeignKey("company.id", ondelete="CASCADE"),
        ),
        default=None
    )
    company: "Company" = Relationship(back_populates="employees")




