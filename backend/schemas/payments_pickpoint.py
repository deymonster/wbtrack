from models.payments_pickpoint import PickpointPaymentsBase
from models.transaction import ITransactionRead
from pydantic import BaseModel
from typing import List, Optional


class IPickpointPaymentsRead(PickpointPaymentsBase):
    total_transactions: Optional[List[ITransactionRead]]
    office_id: int


class IPickpointPaymentsCreate(PickpointPaymentsBase):
    
    office_id: int


class IPickpointPaymentsUpdate(PickpointPaymentsBase):
    id: int
