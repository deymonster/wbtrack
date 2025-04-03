import logging

from fastapi import HTTPException
from fastapi_pagination import LimitOffsetParams
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from crud.base import CRUDBase
from enums.common import ListOrderEnum
from models.company import Company
from models.company_user import CompanyUser
from models.employee import Employee, EmployeeOfficeLink
from models.office import Office
from schemas.office import IOfficeCreate, IOfficeUpdate
from schemas.response import IResponsePaginated

logger = logging.getLogger(__name__)


class OfficeCRUD(CRUDBase[Office, IOfficeCreate, IOfficeUpdate]):
    async def get_by_office_id(self, office_id: int, db_session: AsyncSession | None = None) -> Office | None:
        """Получить офис по office_id."""

        session: AsyncSession = db_session or self.db.session

        query = select(Office).where(Office.office_id == office_id)
        result = await session.execute(query)
        office = result.scalar_one_or_none()

        return office

    async def get_by_external_id(self, external_id: int, db_session: AsyncSession | None = None) -> Office | None:
        """Получение офиса по external_id"""
        session: AsyncSession = db_session or self.db.session

        query = select(Office).where(Office.external_id == external_id)
        result = await session.execute(query)
        office = result.scalar_one_or_none()

        return office


    async def get_all_offices(self, db_session: AsyncSession | None = None) -> list[Office]:
        """Загрузка всех офисов в виде словаря {external_id: Office}"""
        session: AsyncSession = db_session or self.db.session
        query = select(Office)
        response = await session.execute(query)
        offices = response.scalars().all()
        return {office.external_id: office for office in offices}


    async def get_employee_by_office_id(self, office_id: int, db_session: AsyncSession | None = None) -> list[Employee]:
        """Получаем всех сотрудников по office_id."""
        session: AsyncSession = db_session or self.db.session
        db_office = await self.get_by_office_id(office_id=office_id, db_session=session)
        if not db_office:
            raise ValueError(f"Office with office_id={office_id} not found in the database.")
        query = (
            select(Employee)
            .join(EmployeeOfficeLink, Employee.id == EmployeeOfficeLink.employee_id)
            .where(EmployeeOfficeLink.office_id == db_office.id)
        )
        response = await session.execute(query)
        return response.scalars().all()

    async def get_offices_paginated(
        self, *,
        user_id: str,
        params: LimitOffsetParams,
        order_by: str = "id",
        order: ListOrderEnum = ListOrderEnum.descendent,
        db_session: AsyncSession | None = None) -> IResponsePaginated[Office]:
        """Получение офисов с пагинацией.

        :param user_id: ID текущего пользователя
        :param params: Параметры пагинации
        :param order_by: Поле сортировки
        :param order: Направление сортировки
        :param db_session: Сессия базы данных
        :return: Страница офисов с информацией о следующей странице
        """
        session: AsyncSession = db_session or self.db.session
        company_user_query = select(CompanyUser).where(CompanyUser.user_id == user_id)

        company_users = (await session.execute(company_user_query)).scalars().all()
        logger.info(f"Found {len(company_users)} companies for user {user_id}")

        # Проверяем офисы в этих компаниях
        query = (
            select(Office)
            .join(Company)
            .join(CompanyUser, CompanyUser.company_id == Company.id)
            .where(CompanyUser.user_id == user_id)
        )
        offices = (await session.execute(query)).scalars().all()
        logger.info(f"Found {len(offices)} offices for user {user_id}")
        return await self.get_multi_paginated_ordered(
            query=query,
            params=params,
            order_by=order_by,
            order=order,
            db_session=session,
        )

    async def get_office_by_user_id(self, *, office_id: int, user_id: UUID4, db_session: AsyncSession | None = None) -> Office:
        """Получаем офис по user_id

        :param office_id: ID офиса
        :param user_id: ID пользователя
        :param db_session: Сессия базы данных
        :return: Офис
        """

        session: AsyncSession = db_session or self.db.session
        query = (
            select(Office)
            .join(Company, Office.company_id == Company.id)
            .join(CompanyUser, CompanyUser.company_id == Company.id)
            .where(Office.office_id == office_id, CompanyUser.user_id == user_id)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def delete_office_by_user(self, *, office_id: int, user_id: UUID4, db_session: AsyncSession | None = None) -> bool:
        """Удаление офиса с проверкой принадлежности пользователю.
        
        Args:
            office_id: ID офиса
            user_id: ID пользователя
            db_session: Сессия базы данных

        Returns:
            bool: True если офис успешно удален

        Raises:
            HTTPException: Если офис не найден или нет прав доступа
        """

        session: AsyncSession = db_session or self.db.session

        office = await self.get(id=office_id, db_session=session)
        if not office:
            raise HTTPException(
                status_code=404,
                detail="Офис не найден"
            )
        office_with_access = await self.get_office_by_user_id(
            office_id=office_id,
            user_id=user_id,
            db_session=session
        )
        if not office_with_access:
            raise HTTPException(
                status_code=403,
                detail="У вас нет прав на удаление этого офиса"
            )
        
        await self.delete(id=office.id, db_session=session)
        return True

office_crud = OfficeCRUD(Office)



__all__ = [
    "office_crud",
]
