from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base import Base


ModelT = TypeVar("ModelT", bound=Base)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)


class BaseRepository(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    def __init__(self, model: type[ModelT], db: Session) -> None:
        self.model = model
        self.db = db

    def get(self, object_id: int) -> ModelT | None:
        return self.db.get(self.model, object_id)

    def list(self, skip: int = 0, limit: int = 100) -> list[ModelT]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, schema: CreateSchemaT, **extra: object) -> ModelT:
        obj = self.model(**schema.model_dump(), **extra)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelT, schema: UpdateSchemaT) -> ModelT:
        for field, value in schema.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelT) -> None:
        self.db.delete(obj)
        self.db.commit()
