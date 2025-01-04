from sqlmodel import Field, Relationship, SQLModel, Column, ForeignKey, Integer, String, Float, DateTime
from models.base import BaseTableID
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime


if TYPE_CHECKING:
    from models.employee import Employee
    from models.office import Office


class OperationBase(SQLModel):
    operation_id: int = Field(unique=True, index=True) 
    operation_type: str
    summ: float
    rids: str
    created: datetime
    currency: str
    description: str
    summ_pickpoint: float

class Operation(OperationBase, BaseTableID, table=True):
    office_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("office.id", ondelete="CASCADE"),
            nullable=True
        )
    )
    office: "Office" = Relationship(back_populates="operations")

    employee_id: Optional[int] = Field(
        default=None,
        sa_column=Column(
            Integer,
            ForeignKey("employee.id", ondelete="CASCADE"),
            nullable=True
        )
    )
    employee: "Employee" = Relationship(back_populates="operations")
    # details: Optional[List["OperationDetails"]] = Relationship(back_populates="operation")


