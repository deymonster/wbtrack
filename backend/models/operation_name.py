from sqlmodel import Field, Relationship, SQLModel, Column, ForeignKey, Integer, String, Float, DateTime, BigInteger, UniqueConstraint
from models.base import BaseTableID
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime

if TYPE_CHECKING:
    from models.categories_operations import Category


class OperationNameBase(SQLModel):
    base_name: str
    description: Optional[str] = None
    external_id: int = Field(unique=True)  
    minus_description: Optional[str] = None
    minus_name: Optional[str] = None
    name: str


class OperationName(OperationNameBase, BaseTableID, table=True):
    category_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("category.id", ondelete="CASCADE"),
            nullable=False
        ) 
    )
    category: "Category" = Relationship(back_populates="operations")

    __table_args__ = (
        UniqueConstraint('external_id', name='operation_name_external_id_key'),
    )