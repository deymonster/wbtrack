from models.company import CompanyBase
from pydantic import BaseModel
from typing import List, Optional


class ICompanyRead(CompanyBase):
    id: int
    users: Optional[List[int]]
    offices: Optional[List[int]]


class ICompanyCreate(CompanyBase):
    pass


class ICompanyUpdate(CompanyBase):
    id: int
