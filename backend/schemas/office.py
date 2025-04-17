from models.office import OfficeBase
from pydantic import BaseModel, Field


class IOfficeRead(OfficeBase):
    id: int


class IOfficeCreate(OfficeBase):
    company_id: int | None


class IOfficeUpdate(OfficeBase):
    id: int

class IOfficeUpdateFromWB(BaseModel):
    id: int = Field(alias="external_id")
    name: str
    latitude: str
    longitude: str
    is_active: bool
    rate: float | None = 0.0

class UpdateOfficesRequest(BaseModel):
    company_id: int
    offices: list[IOfficeUpdateFromWB]
