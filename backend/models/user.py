from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import Relationship, Field, SQLModel
from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from models.base import BaseTable
from models.company_user import CompanyUser
from enums.user import UserRoleEnum

from fastapi_users.db import SQLAlchemyBaseOAuthAccountTableUUID


if TYPE_CHECKING:
    from models.company import Company
    from models.employee import Employee


class UserBase(SQLModel):
    first_name: str | None
    last_name: str | None
    middle_name: str | None
    phone: str | None
    tg_id: str | None
    role: UserRoleEnum = Field(UserRoleEnum.MANAGER, description="Role of the user")
    
    # Subscription fields (for ADMIN role)
    is_subscription_active: bool = Field(default=False, nullable=True, description="Whether user's subscription is active")
    subscription_start_date: datetime | None = Field(default=None, description="When subscription started")
    subscription_end_date: datetime | None = Field(default=None, description="When subscription ends")
    subscription_approved_by: str | None = Field(default=None, description="ID of super admin who approved subscription")
    subscription_approved_at: datetime | None = Field(default=None, description="When subscription was approved")
    
    # User management fields
    created_by_id: str | None = Field(default=None, description="ID of admin who created this user")
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=True, description="When user was created")
    parent_admin_id: str | None = Field(default=None, description="ID of admin who manages this user (for MANAGER and CHECKER roles)")


class User(UserBase, SQLModelBaseUserDB, BaseTable, table=True):
    companies: list["Company"] = Relationship(
        back_populates="users",
        link_model=CompanyUser,
    )
    
    # Add relationship to created users (for ADMIN role)
    created_users: list["User"] = Relationship(
        back_populates="created_by",
        sa_relationship_kwargs={
            "primaryjoin": "User.id==foreign(User.created_by_id)",
            "remote_side": "[User.id]"
        }
    )
    created_by: Optional["User"] = Relationship(
        back_populates="created_users",
        sa_relationship_kwargs={
            "primaryjoin": "User.id==foreign(User.created_by_id)",
            "remote_side": "[User.created_by_id]"
        }
    )
    
    # Add relationship to parent admin (for MANAGER and CHECKER roles)
    managed_users: list["User"] = Relationship(
        back_populates="parent_admin",
        sa_relationship_kwargs={
            "primaryjoin": "User.id==foreign(User.parent_admin_id)",
            "remote_side": "[User.id]"
        }
    )
    parent_admin: Optional["User"] = Relationship(
        back_populates="managed_users",
        sa_relationship_kwargs={
            "primaryjoin": "User.id==foreign(User.parent_admin_id)",
            "remote_side": "[User.parent_admin_id]"
        }
    )





