from uuid import UUID

from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as SAUUID
from sqlmodel import Field

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
            SAUUID(as_uuid=True),
            ForeignKey("user.id", ondelete="CASCADE"),
            primary_key=True,
        )
    )
