import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from models.categories_operations import Category
from crud.base import CRUDBase
from schemas.categories_operation import ICategoryOperationCreate, ICategoryOperationUpdate

logger = logging.getLogger(__name__)

class CategoriesOperationCRUD(CRUDBase[Category, ICategoryOperationCreate, ICategoryOperationUpdate]):
    async def get_by_external_id(self, external_id: int, db_session: AsyncSession | None = None) -> Category | None:
        """Получение категории по external_id
        
        :param external_id: External_id категории
        :param session: Сессия
        :return: Категория если существует иначе None
        """
        session: AsyncSession = db_session or self.db.session
        query = select(Category).where(Category.external_id == external_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


categories_operation_crud = CategoriesOperationCRUD(Category)  # type: ignore

__all__ = [
    "categories_operation_crud",
]