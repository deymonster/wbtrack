from models.employee import Employee, EmployeeOfficeLink
from models.office import Office
from models.company import Company
from models.company_user import CompanyUser
from crud.base import CRUDBase
from schemas.employee import IEmployeeRead, IEmployeeCreate, IEmployeeUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select, text
from pydantic import UUID4
import logging
from typing import List
from fastapi_pagination import LimitOffsetParams, Page
from enums.common import ListOrderEnum
from schemas.response import IResponsePaginated

from sqlalchemy.engine import Engine
from sqlalchemy.sql import Select

logger = logging.getLogger(__name__)


class EmployeeCRUD(CRUDBase[Employee, IEmployeeCreate, IEmployeeUpdate]):
    async def get_by_phone(self,
                           phone: str,
                           db_session: AsyncSession | None = None) -> Employee | None:
        """Check if an employee with the given phone exists.

        :param phone: The employee's phone number.
        :param db_session: The database session.
        :return: The employee if it exists. Otherwise, None.
        """
        session: AsyncSession = db_session or self.db.session
        query = select(Employee).where(col(Employee.phone) == phone)
        response = await session.execute(query)
        return response.scalar_one_or_none()

    async def get_by_employee_id(self, employee_id: int, db_session: AsyncSession | None = None) -> Employee | None:
        """Получение сотрудника по employee_id."""
        session: AsyncSession = db_session or self.db.session
        
        query = select(Employee).where(Employee.user_id == employee_id)
        result = await session.execute(query)
        employee = result.scalar_one_or_none()
        
        return employee

    async def get_all_employees(self, db_session: AsyncSession | None = None) -> list[Employee]:
        """Получение всех сотрудников в виде словаря {user_id: Employee}"""
        session: AsyncSession = db_session or self.db.session
        query = select(Employee)
        response = await session.execute(query)
        employees = response.scalars().all()
        return {employee.user_id: employee for employee in employees}

    async def get_offices_by_employee_id(self, employee_id: int, db_session: AsyncSession | None = None) -> list[Office]:
        """Получить офисы по employee_id."""
        session: AsyncSession = db_session or self.db.session

        db_employee = await self.get_by_employee_id(employee_id=employee_id, db_session=session)
        if not db_employee:
            raise ValueError(f"Employee with employee_id={employee_id} not found in the database.")
        query = (
            select(Office)
            .join(EmployeeOfficeLink, Office.id == EmployeeOfficeLink.office_id)
            .where(EmployeeOfficeLink.employee_id == db_employee.id)
        )
        response = await session.execute(query)
        return response.scalars().all()

    async def get_employees_by_user_id(self, user_id: UUID4, 
                                       params: LimitOffsetParams | None = LimitOffsetParams(),
                                       order_by: str = "id",
                                       order: ListOrderEnum = ListOrderEnum.descendent,
                                       db_session: AsyncSession | None = None) -> IResponsePaginated[Employee]:
        """Получение связанных сотрудников пользователя
        
        :param user_id: ID пользователя
        :param params: Параметры пагинации
        :param order_by: Поле сортировки
        :param order: Направление сортировки
        :param db_session: Сессия базы данных
        :return: Страница сотрудников
        """
        session: AsyncSession = db_session or self.db.session

        # Условие соединения: связываем Employee через Office и Company с User
        # Формируем запрос с цепочкой join
        join_conditions = [
            (EmployeeOfficeLink, Employee.id == EmployeeOfficeLink.employee_id),
            (Office, EmployeeOfficeLink.office_id == Office.id),
            (Company, Office.company_id == Company.id),
            (CompanyUser, Company.id == CompanyUser.company_id)
        ]

        # Дополнительный фильтр по user_id
        filters = [
            CompanyUser.user_id == user_id
        ]
        query = await self.get_related_objects(
            related_model=Employee,
            join_conditions=join_conditions,
            filters=filters
        )
        query = query.distinct(Employee.id)



        return await self.get_multi_paginated_ordered(
            query=query,
            params=params,
            order_by=order_by,
            order=order,
            db_session=db_session
        )




employee_crud = EmployeeCRUD(Employee)


__all__ = [
    "employee_crud",
]