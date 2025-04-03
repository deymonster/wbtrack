from models.office import OfficeBase


class IOfficeRead(OfficeBase):
    id: int


class IOfficeCreate(OfficeBase):
    company_id: int | None


class IOfficeUpdate(OfficeBase):
    id: int
