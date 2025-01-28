from sqlmodel import Field, Relationship, SQLModel, Column, ForeignKey, Integer, String, Float, DateTime, BigInteger, UniqueConstraint
from models.base import BaseTableID
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, date

if TYPE_CHECKING:
    from models.transaction import Transaction
    from models.office import Office


class PickpointPaymentsBase(SQLModel):
    base_accrued: float
    expensive_accrued: float
    other_accrued: float
    total: float

class PickpointPayments(PickpointPaymentsBase, BaseTableID, table=True):
    __table_args__ = (
        UniqueConstraint("office_id", "weekly_payments_id", name="unique_office_weekly"),
    )
    total_transactions: List["Transaction"] = Relationship(
        back_populates="pickpoint_payments",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
    office_id: int = Field(
    sa_column=Column(
        Integer,
        ForeignKey("office.id", ondelete="CASCADE"),
        nullable=False,
    )
    )
    office: "Office" = Relationship(back_populates="pickpoint_payments")

    weekly_payments_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("weekly_payments.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    weekly_payments: "WeeklyPayments" = Relationship(back_populates="pickpoint_payments")
