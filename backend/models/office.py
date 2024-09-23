from sqlmodel import (
    Field,
    Relationship,
    SQLModel,
    Column,
    ForeignKey,
    Integer)
from models.base import BaseTableID
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from models.company import Company


class OfficeBase(SQLModel):
    office_id: int | None = Field(default=None, alias="id", sa_column=Column(Integer, unique=True, index=True))
    is_site_active: bool = Field(default=True)
    name: str
    office_shk: str


class Office(OfficeBase, BaseTableID, table=True):
    company_id: int | None = Field(
        sa_column=Column(
            Integer,
            ForeignKey("company.id", ondelete="CASCADE"),
        ),
        default=None,
    )
    company: "Company" = Relationship(back_populates="offices")


