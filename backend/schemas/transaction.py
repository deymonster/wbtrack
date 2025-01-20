from models.transaction import TransactionBase
from pydantic import BaseModel
from typing import List, Optional


class ITransactionBaseRead(TransactionBase):
    operation_name: Optional[str]
    weekly_payments_id: Optional[int]
    pickpoint_payments_id: Optional[int]


class ITransactionBaseCreate(TransactionBase):
    operation_name_id: int
    weekly_payments_id: int
    pickpoint_payments_id: int


class ITransactionBaseUpdate(TransactionBase):
    id: int
