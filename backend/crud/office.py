from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from models.office import Office
from crud.base import CRUDBase
from schemas.office import IOfficeRead, IOfficeCreate, IOfficeUpdate


class OfficeCRUD(CRUDBase[Office, IOfficeCreate, IOfficeUpdate]):
    pass


office_crud = OfficeCRUD(Office)


__all__ = [
    "office_crud",
]