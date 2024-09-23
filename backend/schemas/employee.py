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
