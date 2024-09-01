from models.office import OfficeBase


class IOfficeRead(OfficeBase):
    id: int


class IOfficeCreate(OfficeBase):
    pass


class IOfficeUpdate(OfficeBase):
    id: int