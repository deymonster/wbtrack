from sqlmodel import Field, Relationship, SQLModel, Column, ForeignKey, Integer, String, Float, DateTime, BigInteger, UniqueConstraint
from models.base import BaseTableID
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, date

if TYPE_CHECKING:
    from models.office import Office
    from models.total_handle import TotalHandle 


class PickPointHandleBase(SQLModel):
    add_shk_count: int # Доплачено кол-во
    add_shk_sum: int # Доплачено на сумму
    currency: str #  Валюта
    expired_shk_count: int # К удержанию кол-во
    expired_shk_sum: int # К удержанию на сумму
    expiring_shk_count: int # пока не понятно для чего это
    expiring_shk_sum: int # пока не понятно для чего это
    hold_shk_count: int # К удержанию кол-во
    hold_shk_sum: int # К удержанию на сумму
    not_accepted_shk_count: int # пока не понятно для чего это
    not_accepted_shk_sum: int # пока не понятно для чего это
    

class PickPointHandle(PickPointHandleBase, BaseTableID, table=True):
    
    office_id: int = Field(
    sa_column=Column(
        Integer,
        ForeignKey("office.id", ondelete="CASCADE"),
        nullable=False,
        )
    )
    total_handle_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("total_handle.id", ondelete="CASCADE"),
            nullable=False,
        )
    )

    office: "Office" = Relationship(back_populates="pickpoint_handle")
    total_handle: "TotalHandle" = Relationship(back_populates="pickpoints")

