from fastapi import status

from app.core.exceptions import AppException, ConflictError
from app.core.security import PasswordHasher, TokenService
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserAdminCreate, UserCreate


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users
        self.passwords = PasswordHasher()
        self.tokens = TokenService()

    def register(self, data: UserCreate):
        if self.users.get_by_email(data.email):
            raise ConflictError("Email is already registered")
        user_data = UserAdminCreate(**data.model_dump())
        return self.users.create(user_data, self.passwords.hash(data.password))

    def authenticate(self, email: str, password: str) -> Token:
        user = self.users.get_by_email(email)
        if not user or not self.passwords.verify(password, user.hashed_password):
            raise AppException("Invalid email or password", status.HTTP_401_UNAUTHORIZED)
        if not user.is_active:
            raise AppException("Inactive account", status.HTTP_403_FORBIDDEN)
        return Token(access_token=self.tokens.create_access_token(user.id))
