from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserAdminCreate


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email.lower()).first()

    def create(self, data: UserAdminCreate, hashed_password: str) -> User:
        user = User(
            email=data.email.lower(),
            full_name=data.full_name,
            hashed_password=hashed_password,
            role=data.role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
