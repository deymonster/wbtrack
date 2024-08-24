from enum import Enum


class UserRoleEnum(str, Enum):
    MANAGER = "manager"
    ADMIN = "admin"
    CHECKER = "checker"
    SUPER_ADMIN = "super_admin"
