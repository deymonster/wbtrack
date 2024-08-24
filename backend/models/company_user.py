from uuid import UUID
from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import GUID, Field
from models.base import BaseTable


class CompanyUser(BaseTable, table=True):
    company_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("company.id", ondelete="CASCADE"),
            primary_key=True,
        )
    )
    user_id: UUID = Field(
        sa_column=Column(
            GUID,
            ForeignKey("user.id", ondelete="CASCADE"),
            primary_key=True,
        )
    )
