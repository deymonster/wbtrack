from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from models.employee import EmployeeBase


class IEmployeeRead(EmployeeBase):
    id: int
    create_date: str = Field(..., description="Дата создания в формате YYYY-MM-DD")

    @field_validator("create_date", mode='before')
    @classmethod
    def format_create_date(cls, value: datetime) -> str:
        """Преобразование даты в строку формата YYYY-MM-DD."""
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")  # Пример: 2025-01-04
        return value


class IEmployeeCreate(EmployeeBase):
    pass


class IEmployeeUpdate(EmployeeBase):
    pass


class RegistrationRequest(BaseModel):
    phone: str
    email: str


class AuthRequest(BaseModel):
    phone: str
    otp: Optional[str] = None


class SearchParams(BaseModel):
    search_field: str
    search_value: str
