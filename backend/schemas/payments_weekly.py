from models.payments_weekly import WeeklyPaymentsBase
from models.transaction import ITransactionRead
from models.payments_pickpoint import IPickpointPaymentsRead
from pydantic import BaseModel
from typing import List, Optional


class IWeeklyPaymentsBaseRead(WeeklyPaymentsBase):
    total_transactions: Optional[List[ITransactionRead]]
    pickpoint_payments: Optional[List[IPickpointPaymentsRead]]


class IWeeklyPaymentsBaseCreate(WeeklyPaymentsBase):
    total_transactions: Optional[List[ITransactionRead]]
    pickpoint_payments: Optional[List[IPickpointPaymentsRead]]


class IWeeklyPaymentsBaseUpdate(WeeklyPaymentsBase):
    id: int
