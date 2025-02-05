import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from models.total_handle import TotalHandle
from crud.base import CRUDBase
from schemas.total_handle import ITransactionBaseRead, ITransactionBaseCreate, ITransactionBaseUpdate
from schemas.pickpoint_handle import IPickPointHandleCreate
from pvz_client.models import TotalHandlingReport

logger = logging.getLogger(__name__)

class TotalHandleCRUD(CRUDBase[TotalHandle, ITransactionBaseCreate, ITransactionBaseUpdate]):
    async def create_total_handle_with_pickpoints(
        self,
        *,
        handle_data: TotalHandlingReport,
        db_session: AsyncSession | None = None
    ) -> TotalHandle:
        """Create total handle with nested pickpoint handles"""
        session: AsyncSession = db_session or self.db.session

        try:
            total_handle_data = ITotalHandleCreate(**handle_data.dict(exclude={'pickpoints'}))
            total_handle = await self.create( obj_in=total_handle_data, db_session=session)
            if handle_data.pickpoints:
                for pp_data in handle_data.pickpoints:
                    office = await office_crud.get_by_external_id(external_id=pp_data.pickpoint_id, db_session=session)

                    if not office:
                        logger.warning(f"Office with external_id={pp_data.pickpoint_id} not found, skipping")
                        raise ValueError(f"Office with external_id={pp_data.pickpoint_id} not found")
                    pickpoint_handle_data = IPickPointHandleCreate(
                        office_id=office.id,
                        total_handle_id=total_handle.id,
                        add_shk_count=pp_data.add_shk_count,
                        add_shk_sum=pp_data.add_shk_sum,
                        currency=pp_data.currency,
                        expired_shk_count=pp_data.expired_shk_count,
                        expired_shk_sum=pp_data.expired_shk_sum,
                        expiring_shk_count=pp_data.expiring_shk_count,
                        expiring_shk_sum=pp_data.expiring_shk_sum,
                        hold_shk_count=pp_data.hold_shk_count,
                        hold_shk_sum=pp_data.hold_shk_sum,
                        not_accepted_shk_count=pp_data.not_accepted_shk_count,
                        not_accepted_shk_sum=pp_data.not_accepted_shk_sum
                    )

                    await pickpoint_handle_crud.create(obj_in=pickpoint_handle_data, db_session=session)
            await session.refresh(total_handle)
            return total_handle
        
        except Exception as e:
            logger.error(f"Error creating total handle: {e}", exc_info=True)
            raise

        



          

total_handle_crud = TotalHandleCRUD(TotalHandle)  # type: ignore


__all__ = [
    "total_handle_crud",
]