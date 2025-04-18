from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlmodel import col, select
from sqlalchemy.orm import selectinload
from core.utils.sqlmodel import relations
from crud.base import CRUDBase
from crud.employee import employee_crud
from crud.office import office_crud
from crud.employee_office_link import employee_office_link_crud
from models.company import Company
from models.user import User
from models.employee import Employee 
from models.office import Office 
from schemas.company import ICompanyCreate, ICompanyUpdate
from schemas.employee import IEmployeeCreate
from schemas.employee_office_link import IEmployeeOfficeLinkCreate
from schemas.office import IOfficeCreate



class CRUDCompany(CRUDBase[Company, ICompanyCreate, ICompanyUpdate]):
    async def get_with_user(
        self,
        *,
        id: int,
        user_id: UUID4,
        db_session: AsyncSession | None = None,
    ) -> Company | None:
        """Get one object by id.

        :param id: The primary key of the model.
        :param db_session: The database session.
        :return: A single object or None
        """
        session: AsyncSession = db_session or self.db.session
        query = select(Company).where(
            col(Company.id) == id,
            relations(Company.users).any(col(User.id) == user_id),
        )
        response = await session.execute(query)
        return response.scalar_one_or_none()

    async def add_user(
        self,
        *,
        company: Company,
        user: User,
        db_session: AsyncSession | None = None,
    ):
        session = db_session or self.db.session

        # Проверяем, связан ли пользователь с компанией
        query = select(Company).where(
            Company.id == company.id,
            relations(Company.users).any(User.id == user.id)
        )
        result = await session.execute(query)
        existing_link = result.scalar_one_or_none()

        # Если связь уже существует, просто возвращаем компанию
        if existing_link:
            return company

        # Если связи нет, добавляем пользователя к компании
        await session.refresh(company, attribute_names=["users"])
        company.users.append(user)
        await session.commit()
        return company

    async def get_company_by_wb_user_id(self, wb_user_id: int, db_session: AsyncSession | None = None) -> Company:
        """Получение компании по wb_user_id"""
        session = db_session or self.db.session
        query = select(Company).where(Company.wb_user_id == wb_user_id)
        result = await session.execute(query)
        company = result.scalar_one_or_none()

        return company

    async def register_company(self, *, owner_info: dict, offices: list, current_user: User, db_session: AsyncSession | None = None) -> Company:
        """Регистрация новой компании со всеми связями"""
        session = db_session or self.db.session

        # 1. Create/Update company
        company = await self.create_or_update(
            obj_in=ICompanyCreate(
                wb_user_id=owner_info.wb_user_id,
                name=owner_info.name,
                phone=str(owner_info.phone),
                org_name=owner_info.org_name,
            ),
            index_elements=["wb_user_id"],
            create_exclude={"id"},
            update_exclude={"id"},
            db_session=session
        )

        # 2. Link company to user
        await self.add_user(company=company, user=current_user, db_session=session)


        # 3. Create/Update employees
        unique_employees = {
            emp.user_id: IEmployeeCreate(
                user_id=emp.user_id,
                name=emp.name,
                last_name=emp.last_name,
                phone=str(emp.phone),
                is_deleted=False
            )
            for office in offices 
            if office.is_active
            for emp in office.users 
            if not emp.is_deleted
        }

        await employee_crud.create_or_update_multi(
            list_in=unique_employees.values(),
            index_elements=["user_id"],
            on_conflict_set={"name", "last_name", "phone", "is_deleted"},
            db_session=session
        )

        employees = await employee_crud.get_multi(
            query=select(Employee).where(
                Employee.user_id.in_([emp.user_id for emp in unique_employees.values()])
            ),
            db_session=session
        )

        # 4. Create/Update offices
        await office_crud.create_or_update_multi(
            list_in=(
                IOfficeCreate(
                    office_id=office.id,
                    name=office.name,
                    latitude=office.latitude,
                    longitude=office.longitude,
                    is_active=True,
                    external_id=office.external_id,
                    rate=office.rate,
                    company_id=company.id
                ) 
                for office in offices 
                if office.is_active
            ),
            index_elements=["office_id"],
            on_conflict_set={"name", "latitude", "longitude", "is_active", "rate"},
            additionals={"company_id": company.id},
            db_session=session
        )

        created_offices = await office_crud.get_multi(
            query=select(Office).where(
                Office.office_id.in_([office.id for office in offices if office.is_active])
            ),
            db_session=session
        )

        # 5. Create employee-office links
        unique_links = [
            IEmployeeOfficeLinkCreate(
                employee_id=next(e.id for e in employees if e.user_id == emp.user_id),
                office_id=next(o.id for o in created_offices if o.office_id == office.id)
            )
            for office in offices
            if office.is_active
            for emp in office.users
            if not emp.is_deleted
        ]

        await employee_office_link_crud.create_multi(
            list_in=unique_links,
            db_session=session
        )

        # 6. Get final result with relationships
        result = await self.get_multi(
            query=(
                select(Company)
                .where(Company.id == company.id)
                .options(
                    selectinload(Company.users),
                    selectinload(Company.offices)
                )
            ),
            db_session=session
        )

        return result[0]


    async def get_or_404(self, *, id: int, db_session: AsyncSession | None = None) -> Company:
        """Получение компании по id"""
        session = db_session or self.db.session
        company =await self.get(id=id, db_session=session)
        if not company:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

        return company

company_crud = CRUDCompany(Company)  # type: ignore


__all__ = [
    "company_crud",
]
