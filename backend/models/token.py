from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4


class Token(SQLModel, table=True):
    """Модель для хранения токенов доступа и обновления"""
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    phone: str = Field(index=True)  # Индексируем по номеру телефона для быстрого поиска
    token_type: str = Field(index=True)  # "access" или "refresh"
    token_value: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True

        