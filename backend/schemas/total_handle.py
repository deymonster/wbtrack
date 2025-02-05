from models.total_handle import TotalHandleBase
from typing import List, Optional

class ITotalHandleRead(TotalHandleBase):
    pass


class ITotalHandleCreate(TotalHandleBase):
    pass


class ITotalHandleUpdate(TotalHandleBase):
    id: int