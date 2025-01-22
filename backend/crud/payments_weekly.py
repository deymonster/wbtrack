import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from models.payments_weekly import WeeklyPayments
from crud.base import CRUDBase
from schemas.payments_weekly import IWeeklyPaymentsBaseRead, IWeeklyPaymentsBaseCreate, IWeeklyPaymentsBaseUpdate

logger = logging.getLogger(__name__)

class WeeklyPaymentsCRUD(CRUDBase[WeeklyPayments, IWeeklyPaymentsBaseCreate, IWeeklyPaymentsBaseUpdate]):
    pass
          

weekly_payments_crud = WeeklyPaymentsCRUD(WeeklyPayments)  # type: ignore


__all__ = [
    "weekly_payments_crud",
]