from models.pickpoint_handle import PickPointHandleBase
from typing import List, Optional

class IPickPointHandleRead(PickPointHandleBase):
    office_id: int
    total_handle_id: int


class IPickPointHandleCreate(PickPointHandleBase):
    office_id: int
    total_handle_id: int


class IPickPointHandleUpdate(PickPointHandleBase):
    id: int