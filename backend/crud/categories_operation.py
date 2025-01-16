import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from models.categories_operations import CategoryOperation
from crud.base import CRUDBase

logger = logging.getLogger(__name__)