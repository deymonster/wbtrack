from datetime import datetime, UTC
from pydantic import field_validator
from sqlalchemy import text
from sqlmodel import Field, SQLModel


class TimestampMixin(SQLModel):

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(None),
        nullable=False,
        sa_column_kwargs={"server_default": text("current_timestamp(0)")},
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(None),
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
            "onupdate": text("current_timestamp(0)"),
        },
    )

    @field_validator("updated_at")
    def validate_updated_at(cls, v):
        if v is None:
            return v
        return v.replace(tzinfo=None)
