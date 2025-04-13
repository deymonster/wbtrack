from datetime import date
from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.office_report import OfficeReport
from schemas.office_report import IOfficeReportCreate, IOfficeReportUpdate
from crud.base import CRUDBase


class OfficeReportCRUD(CRUDBase[OfficeReport, IOfficeReportCreate, IOfficeReportUpdate]):
    async def get_by_date_range(self, office_id: int, start_date: date, end_date: date, db_session: AsyncSession | None = None) -> List[OfficeReport]:
        """Получение отчетов по диапазону дат для офиса"""

        session = db_session or self.db_session
        query = select(OfficeReport).where(
            OfficeReport.office_id == office_id,
            OfficeReport.report_date >= start_date,
            OfficeReport.report_date <= end_date
        )
        result = await session.execute(query)
        return result.scalars().all()

    async def get_by_date(self, office_id: int, report_date: date, db_session: AsyncSession | None = None) -> OfficeReport | None:
        """Получение отчета по дате для офиса"""
        session = db_session or self.db_session
        query = select(OfficeReport).where(
            OfficeReport.office_id == office_id,
            OfficeReport.report_date == report_date
        )
        result = await session.execute(query)
        return result.scalars().first()

        
office_report_crud = OfficeReportCRUD(OfficeReport)