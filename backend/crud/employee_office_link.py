from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from crud.base import CRUDBase
from models.employee import EmployeeOfficeLink
from schemas.employee_office_link import (
    IEmployeeOfficeLinkCreate,
    IEmployeeOfficeLinkRead,
)


class CRUDEmployeeOfficeLink(CRUDBase[EmployeeOfficeLink, IEmployeeOfficeLinkCreate, IEmployeeOfficeLinkRead]):
    async def create_link(
        self,
        employee_id: int,
        office_id: int,
        db_session: AsyncSession | None = None,
    ) -> EmployeeOfficeLink:
        session: AsyncSession = db_session or self.db.session
        link = EmployeeOfficeLink(employee_id=employee_id, office_id=office_id)
        session.add(link)
        await session.commit()
        await session.refresh(link)
        return link

    async def get_link(
        self,
        employee_id: int,
        office_id: int,
        db_session: AsyncSession | None = None,
    ) -> EmployeeOfficeLink | None:
        session: AsyncSession = db_session or self.db.session
        query = select(EmployeeOfficeLink).where(
        EmployeeOfficeLink.employee_id == employee_id,
        EmployeeOfficeLink.office_id == office_id
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()



employee_office_link_crud = CRUDEmployeeOfficeLink(EmployeeOfficeLink)
