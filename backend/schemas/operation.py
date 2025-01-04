from models.operation import OperationBase
from typing import Optional


class IOperationCreate(OperationBase):
    office_id: Optional[int] = None
    employee_id: Optional[int] = None

class IOperationRead(OperationBase):
    id: int
