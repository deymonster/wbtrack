from sqlmodel import Field, Relationship, SQLModel, Column, ForeignKey, Integer, String, Float, DateTime, BigInteger, UniqueConstraint
from models.base import BaseTableID
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, date

if TYPE_CHECKING:
    from models.transaction import Transaction


class PickpointPaymentsBase(SQLModel):
    base_accrued: float
    expensive_accrued: float
    other_accrued: float
    total: float

class PickpointPayments(PickpointPaymentsBase, BaseTableID, table=True):
    total_transactions: List["Transaction"] = Relationship(
        back_populates="pickpoint_payments",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )
