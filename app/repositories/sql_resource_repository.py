from collections.abc import Callable
from dataclasses import is_dataclass, replace
from typing import Any, Generic, TypeVar
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base

TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel", bound=Base)


class SqlResourceRepository(Generic[TEntity, TModel]):
    """
    Generic SQLAlchemy CRUD repository for admin resources.

    @param session_factory: SQLAlchemy session factory
    @param model_cls: ORM model class
    @param to_entity: ORM -> domain mapper
    @param to_model: domain -> ORM mapper
    @param field_map: Optional domain field to ORM attribute map
    """

    def __init__(
        self,
        session_factory: sessionmaker[Session],
        model_cls: type[TModel],
        to_entity: Callable[[TModel], TEntity],
        to_model: Callable[[TEntity], TModel],
        field_map: dict[str, str] | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._model_cls = model_cls
        self._to_entity = to_entity
        self._to_model = to_model
        self._field_map = field_map or {}

    def list(self, *, active_only: bool = False) -> list[TEntity]:
        """
        @param active_only: When True, keep only active rows
        @return: List of entities
        """
        with self._session_factory() as session:
            rows = list(session.scalars(select(self._model_cls)).all())
            if active_only:
                rows = [row for row in rows if getattr(row, "active", True)]
            return [self._to_entity(row) for row in rows]

    def get_by_id(self, item_id: str) -> TEntity | None:
        """
        @param item_id: Entity id
        @return: Entity or None
        """
        with self._session_factory() as session:
            row = session.get(self._model_cls, item_id)
            return self._to_entity(row) if row else None

    def create(self, item: TEntity) -> TEntity:
        """
        @param item: Entity to persist
        @return: Stored entity
        """
        with self._session_factory() as session:
            item_id = getattr(item, "id", None) or str(uuid4())
            if session.get(self._model_cls, item_id):
                raise ValueError(f"Id already exists: {item_id}")
            if is_dataclass(item) and getattr(item, "id", None) != item_id:
                item = replace(item, id=item_id)  # type: ignore[arg-type]
            row = self._to_model(item)
            session.add(row)
            session.commit()
            session.refresh(row)
            return self._to_entity(row)

    def update(self, item_id: str, **changes: Any) -> TEntity:
        """
        @param item_id: Entity id
        @param changes: Fields to update
        @return: Updated entity
        """
        with self._session_factory() as session:
            row = session.get(self._model_cls, item_id)
            if not row:
                raise KeyError(item_id)
            for key, value in changes.items():
                if value is None:
                    continue
                attr = self._field_map.get(key, key)
                if hasattr(row, attr):
                    setattr(row, attr, value)
            session.commit()
            session.refresh(row)
            return self._to_entity(row)

    def delete(self, item_id: str) -> None:
        """
        @param item_id: Entity id
        @return: None
        """
        with self._session_factory() as session:
            row = session.get(self._model_cls, item_id)
            if not row:
                raise KeyError(item_id)
            session.delete(row)
            session.commit()
