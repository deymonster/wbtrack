from models.employee import Employee
from models.office import Office
from crud.base import CRUDBase
from schemas.employee import IEmployeeRead, IEmployeeCreate, IEmployeeUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select, text
import logging

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


employee_crud = EmployeeCRUD(Employee)


__all__ = [
    "employee_crud",
]