from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"
