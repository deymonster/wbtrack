from enum import Enum


class UserRoleEnum(str, Enum):
    MANAGER = "manager"  # Basic role with minimal permissions
    CHECKER = "checker"  # Role for checking operations, created by admin
    ADMIN = "admin"  # Admin with subscription-based permissions
    SUPER_ADMIN = "super_admin"  # Super admin with full access
