import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from models.payments_pickpoint import PickpointPayments
from crud.base import CRUDBase
from schemas.payments_pickpoint import IPickpointPaymentsRead, IPickpointPaymentsCreate, IPickpointPaymentsUpdate

logger = logging.getLogger(__name__)

class PickpointPaymentsCRUD(CRUDBase[PickpointPayments, IPickpointPaymentsCreate, IPickpointPaymentsUpdate]):
    pass
          

pickpoint_payments_crud = PickpointPaymentsCRUD(PickpointPayments)  # type: ignore


__all__ = [
    "pickpoint_payments_crud",
]