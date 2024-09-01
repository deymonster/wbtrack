from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select

from core.utils.sqlmodel import relations
from crud.base import CRUDBase
from models.company import Company
from models.user import User
from schemas.company import ICompanyRead, ICompanyCreate, ICompanyUpdate


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
        await session.refresh(company, attribute_names=["users"])
        company.users.append(user)
        await session.commit()
        return company


company_crud = CRUDCompany(Company)  # type: ignore


__all__ = [
    "company_crud",
]