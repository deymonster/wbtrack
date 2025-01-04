from models.operation import Operation
from crud.base import CRUDBase
from schemas.operation import IOperationCreate, IOperationRead



class OperationCRUD(CRUDBase[Operation, IOperationCreate, IOperationRead]):
    pass



operation_crud = OperationCRUD(Operation)  # type: ignore


__all__ = [
    "operation_crud",
]