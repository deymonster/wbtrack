import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from models.operation_name import OperationName
from crud.base import CRUDBase
from schemas.operation_name import IOperationNameRead, IOperationNameCreate, IOperationNameUpdate

logger = logging.getLogger(__name__)

class OperationNameCRUD(CRUDBase[OperationName, IOperationNameCreate, IOperationNameUpdate]):

    async def get_operations_by_category_external_id(
            self, 
            *,
            db_session: AsyncSession | None = None,
            category_external_id: int) -> list[OperationName] | None:
            """Получение всех операций по external_id категории
            
            :param session: Сессия
            :param category_external_id: External_id категории
            :return: Список операций
            """

            session: AsyncSession = db_session or self.db.session

            query = (
                select(OperationName)
                .where(OperationName.category.has(external_id=category_external_id))
                )
            result = await session.execute(query)
            return result.scalars().all()

           


operation_name_crud = OperationNameCRUD(OperationName)  # type: ignore


__all__ = [
    "operation_name_crud",
]