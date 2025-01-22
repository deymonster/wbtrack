from sqlmodel import Field, Relationship, SQLModel, Column, ForeignKey, Integer, String, Float, DateTime, BigInteger, UniqueConstraint
from models.base import BaseTableID
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, date

if TYPE_CHECKING:
    from models.operation_name import OperationName
    from models.payments_weekly import WeeklyPayments
    from models.payments_pickpoint import PickpointPayments
    from models.office import Office


class TransactionBase(SQLModel):
    sum: float
    count: int
    


class Transaction(TransactionBase, BaseTableID, table=True):
    operation_name_id: int = Field (
        sa_column=Column(
            Integer,
            ForeignKey("operation_name.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    operation_name: "OperationName" = Relationship(back_populates="transactions")

    weekly_payments_id: int = Field (
        sa_column=Column(
            Integer,
            ForeignKey("weekly_payments.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    weekly_payments: Optional["WeeklyPayments"] = Relationship(
        back_populates="total_transactions"
    )

    pickpoint_payments_id: int = Field (
        sa_column=Column(
            Integer,
            ForeignKey("pickpoint_payments.id", ondelete="CASCADE"),
            nullable=False,
        )
    )
    pickpoint_payments: Optional["PickpointPayments"] = Relationship(
        back_populates="total_transactions"
    )




    
