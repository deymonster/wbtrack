from typing import Optional

from models.employee import EmployeeBase
from pydantic import BaseModel


class IEmployeeRead(EmployeeBase):
    id: int


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
