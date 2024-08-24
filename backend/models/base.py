import re
from uuid import UUID

from sqlalchemy import text
from sqlmodel import GUID, Field, SQLModel
from models.base_mixin import TimestampMixin


class BaseTable(SQLModel):
    @classmethod
    @property
    def __tablename__(cls):
        class_name = cls.__name__
        words = re.findall("[A-Z][^A-Z]*", class_name)
        return "_".join([word.lower() for word in words])

    def model_update(self, **update_data):
        for field in update_data:
            if not field in self.model_fields:
                continue
            setattr(self, field, update_data[field])
        return self


class BaseTableUUID(BaseTable, TimestampMixin):
    id: UUID = Field(
        default=None,
        primary_key=True,
        sa_type=GUID,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )


class BaseTableID(BaseTable, TimestampMixin):
    id: int = Field(
        default=None,
        primary_key=True,
        nullable=False,
    )
