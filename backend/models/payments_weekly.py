from sqlmodel import Field, Relationship, SQLModel, Column, ForeignKey, Integer, String, Float, DateTime, BigInteger, UniqueConstraint
from models.base import BaseTableID
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, date

if TYPE_CHECKING:
    from models.transaction import Transaction
    from models.payments_pickpoint import PickpointPayments


class WeeklyPaymentsBase(SQLModel):
    base_accrued: float
    date_from: date = Field(index=True)
    date_to: date = Field(index=True)
    expensive_accrued: float
    other_accrued: float
    total: float

class WeeklyPayments(WeeklyPaymentsBase, BaseTableID, table=True):
    __table_args__ = (
        UniqueConstraint("date_from", "date_to", name="unique_date_from_date_to"),
    )
    total_transactions: List["Transaction"] = Relationship(
        back_populates="weekly_payments",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
    pickpoint_payments: List["PickpointPayments"] = Relationship(
        back_populates="weekly_payments",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
