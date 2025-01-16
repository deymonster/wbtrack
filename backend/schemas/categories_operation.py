from models.categories_operations import CategoryBase
from pydantic import BaseModel
from typing import List, Optional


class ICategoryOperationRead(CategoryBase):
    operations: List[int]


class ICategoryOperationCreate(CategoryBase):
    pass


class ICategoryOperationUpdate(CategoryBase):
    id: int
