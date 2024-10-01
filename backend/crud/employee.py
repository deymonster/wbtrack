from models.employee import Employee
from crud.base import CRUDBase
from schemas.employee import IEmployeeRead, IEmployeeCreate, IEmployeeUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select, text


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
        query = select(Employee).where(text(':phone = ANY(phones)'))
        # query = select(Employee).where(phone == col(Employee.phones.any()))
        response = await session.execute(query, {'phone': phone})
        return response.scalar_one_or_none()


employee_crud = EmployeeCRUD(Employee)


__all__ = [
    "employee_crud",
]