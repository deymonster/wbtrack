from models.company import CompanyBase


class ICompanyRead(CompanyBase):
    id: int


class ICompanyCreate(CompanyBase):
    pass


class ICompanyUpdate(CompanyBase):
    id: int
