from sqlmodel import Field, Relationship, SQLModel, Column, ForeignKey, Integer, String, Float, DateTime, BigInteger, UniqueConstraint
from models.base import BaseTableID
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, date

if TYPE_CHECKING:
    from models.pickpoint_handle import PickPointHandle


class TotalHandleBase(SQLModel):
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
    payments_suspended: bool
    

class TotalHandle(TotalHandleBase, BaseTableID, table=True):
    
    pickpoints: List["PickPointHandle"] = Relationship(
        back_populates="total_handle",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )


