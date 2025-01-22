import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from models.payments_pickpoint import PickpointPayments
from crud.base import CRUDBase
from schemas.payments_pickpoint import IPickpointPaymentsBaseRead, IPickpointPaymentsBaseCreate, IPickpointPaymentsBaseUpdate

logger = logging.getLogger(__name__)

class PickpointPaymentsCRUD(CRUDBase[PickpointPayments, IPickpointPaymentsBaseCreate, IPickpointPaymentsBaseUpdate]):
    pass
          

pickpoint_payments_crud = PickpointPaymentsCRUD(PickpointPayments)  # type: ignore


__all__ = [
    "pickpoint_payments_crud",
]