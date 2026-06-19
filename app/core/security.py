from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher:
    def hash(self, password: str) -> str:
        return password_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return password_context.verify(plain_password, hashed_password)


class TokenService:
    def create_access_token(self, subject: str | int, expires_delta: timedelta | None = None) -> str:
        expire = datetime.now(timezone.utc) + (
            expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        payload: dict[str, Any] = {"sub": str(subject), "exp": expire}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def decode_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def decode_token_subject(token: str) -> int | None:
    try:
        payload = TokenService().decode_token(token)
        subject = payload.get("sub")
        return int(subject) if subject is not None else None
    except (JWTError, ValueError):
        return None
