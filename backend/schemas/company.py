from typing import List, Optional

from models.company import CompanyBase
from schemas.user import IUserRead
from schemas.office import IOfficeRead


class ICompanyRead(CompanyBase):
    id: int
    users: Optional[List[IUserRead]]
    offices: Optional[List[IOfficeRead]]


class ICompanyCreate(CompanyBase):
    pass


class ICompanyUpdate(CompanyBase):
    id: int
