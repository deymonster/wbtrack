from sqlmodel import Field, Relationship, SQLModel, Column, ForeignKey, Integer, String, Float, DateTime, BigInteger
from models.base import BaseTableID
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime

if TYPE_CHECKING:
    from models.operation_name import OperationName


class CategoryBase(SQLModel):
    external_id: int = Field(sa_column=Column(Integer, unique=True, index=True))
    name: str = Field(sa_column=Column(String, index=True))
    description: Optional[str] = Field(default=None, sa_column=Column(String))

class Category(CategoryBase, BaseTableID, table=True):
    operations: List["OperationName"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"cascade": "all, delete"}
    )