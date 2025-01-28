from models.payments_pickpoint import PickpointPaymentsBase
from schemas.transaction import ITransactionBaseRead
from pydantic import BaseModel
from typing import List, Optional


class IPickpointPaymentsRead(PickpointPaymentsBase):
    total_transactions: Optional[List[ITransactionBaseRead]]
    office_id: int


class IPickpointPaymentsCreate(PickpointPaymentsBase):
    weekly_payments_id: int
    office_id: int


class IPickpointPaymentsUpdate(PickpointPaymentsBase):
    id: int
