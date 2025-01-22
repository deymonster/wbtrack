import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from models.transaction import Transaction
from crud.base import CRUDBase
from schemas.transaction import ITransactionBaseRead, ITransactionBaseCreate, ITransactionBaseUpdate

logger = logging.getLogger(__name__)

class TransactionCRUD(CRUDBase[Transaction, ITransactionBaseCreate, ITransactionBaseUpdate]):
    pass
          

transaction_crud = TransactionCRUD(Transaction)  # type: ignore


__all__ = [
    "transaction_crud",
]