import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from models.pickpoint_handle import PickPointHandle
from crud.base import CRUDBase
from schemas.pickpoint_handle import IPickPointHandleRead, IPickPointHandleCreate, IPickPointHandleUpdate

logger = logging.getLogger(__name__)

class PickPointHandleCRUD(CRUDBase[PickPointHandle, IPickPointHandleCreate, IPickPointHandleUpdate]):
    pass
          

pickpoint_handle_crud = PickPointHandleCRUD(PickPointHandle)  # type: ignore


__all__ = [
    "pickpoint_handle_crud",
]