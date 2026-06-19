from collections.abc import Callable

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.enums import UserRole
from app.core.exceptions import AppException, ForbiddenError
from app.core.security import decode_token_subject
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_PREFIX}/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    user_id = decode_token_subject(token)
    if not user_id:
        raise AppException("Invalid authentication credentials", status.HTTP_401_UNAUTHORIZED)
    user = UserRepository(db).get(user_id)
    if not user or not user.is_active:
        raise AppException("Invalid authentication credentials", status.HTTP_401_UNAUTHORIZED)
    return user


def require_roles(*roles: UserRole) -> Callable[[User], User]:
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise ForbiddenError()
        return current_user

    return checker
