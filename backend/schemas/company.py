from models.company import CompanyBase
from pydantic import BaseModel


class ICompanyRead(CompanyBase):
    id: int


class ICompanyCreate(CompanyBase):
    pass


class ICompanyUpdate(CompanyBase):
    id: int
