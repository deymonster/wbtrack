from typing import List, Optional

from models.company import CompanyBase


class ICompanyRead(CompanyBase):
    id: int
    users: Optional[List[int]]
    offices: Optional[List[int]]


class ICompanyCreate(CompanyBase):
    pass


class ICompanyUpdate(CompanyBase):
    id: int
