from models.payments_weekly import WeeklyPaymentsBase
from schemas.transaction import ITransactionBaseRead
from schemas.payments_pickpoint import IPickpointPaymentsRead
from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class IWeeklyPaymentsBaseRead(WeeklyPaymentsBase):
    total_transactions: Optional[List[ITransactionBaseRead]]
    pickpoint_payments: Optional[List[IPickpointPaymentsRead]]


class IWeeklyPaymentsBaseCreate(WeeklyPaymentsBase):
    date_from: date
    date_to: date


class IWeeklyPaymentsBaseUpdate(WeeklyPaymentsBase):
    id: int
