from models.operation_name import OperationNameBase
from pydantic import BaseModel
from typing import List, Optional


class IOperationNameRead(OperationNameBase):
    pass


class IOperationNameCreate(OperationNameBase):
    category_id: int


class IOperationNameUpdate(OperationNameBase):
    id: int
