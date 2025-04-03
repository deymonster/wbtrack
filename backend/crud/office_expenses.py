from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.office_expenses import OfficeExpenses
from crud.base import CRUDBase
from crud.office import office_crud 
from schemas.office_expenses import (
    IOfficeExpensesRead,
    IOfficeExpensesCreate,
    IOfficeExpensesUpdate
)



class OfficeExpensesCRUD(CRUDBase[OfficeExpenses, IOfficeExpensesCreate, IOfficeExpensesUpdate]):
    async def verify_office_access(self, office_id: int, user_id: int, db_session: AsyncSession | None = None) -> None:
        """Проверка доступа пользователя к офису"""
        session: AsyncSession = db_session or self.db.session
        office = await office_crud.get_office_by_user_id(office_id=office_id, user_id=user_id)
        if not office:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Office not found or you don't have access to it"
            )
        

    async def get_expenses_or_404(self, office_id: int, db_session: AsyncSession | None = None) -> OfficeExpenses:
        """Получение office expenses по office_id или 404"""
        session: AsyncSession = db_session or self.db.session
        expenses = await self.get_by_office_id(office_id=office_id)
        if not expenses:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Office expenses not found for this office")
        return expenses

    
    async def get_by_office_id(self, office_id: int, db_session: AsyncSession | None = None) -> OfficeExpenses | None:
        """Получаем office expenses by office id
        
        :param office_id: int
        :param db: AsyncSession
        :return: OfficeExpenses | None
        """

        session: AsyncSession = db_session or self.db.session

        query = select(OfficeExpenses).where(OfficeExpenses.office_id == office_id)
        result = await session.execute(query)
        office_expenses = result.scalar_one_or_none()
        return office_expenses



office_expenses_crud = OfficeExpensesCRUD(OfficeExpenses)