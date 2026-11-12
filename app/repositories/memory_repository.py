from copy import deepcopy
from dataclasses import fields, replace
from typing import Generic, TypeVar
from uuid import uuid4

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    """
    Generic in-memory CRUD repository.

    @param seed: Optional initial entities
    """

    def __init__(self, seed: list[T] | None = None) -> None:
        """
        @param seed: Optional initial entities
        @return: None
        """
        self._items: dict[str, T] = {}
        for item in seed or []:
            item_id = getattr(item, "id")
            self._items[item_id] = deepcopy(item)

    def list(self, *, active_only: bool = False) -> list[T]:
        """
        @param active_only: When True, keep only active rows
        @return: List of entities
        """
        items = list(self._items.values())
        if active_only:
            items = [item for item in items if getattr(item, "active", True)]
        return [deepcopy(item) for item in items]

    def get_by_id(self, item_id: str) -> T | None:
        """
        @param item_id: Entity id
        @return: Entity copy or None
        """
        item = self._items.get(item_id)
        return deepcopy(item) if item else None

    def create(self, item: T) -> T:
        """
        @param item: Entity to persist
        @return: Stored entity copy
        """
        item_id = getattr(item, "id") or str(uuid4())
        if hasattr(item, "id"):
            item = replace(item, id=item_id)  # type: ignore[arg-type]
        if item_id in self._items:
            raise ValueError(f"Id already exists: {item_id}")
        self._items[item_id] = deepcopy(item)
        return deepcopy(item)

    def update(self, item_id: str, **changes) -> T:
        """
        @param item_id: Entity id
        @param changes: Fields to update
        @return: Updated entity copy
        """
        current = self._items.get(item_id)
        if not current:
            raise KeyError(item_id)
        allowed = {field.name for field in fields(current)}  # type: ignore[arg-type]
        payload = {key: value for key, value in changes.items() if key in allowed and value is not None}
        updated = replace(current, **payload)  # type: ignore[arg-type]
        self._items[item_id] = updated
        return deepcopy(updated)

    def delete(self, item_id: str) -> None:
        """
        @param item_id: Entity id
        @return: None
        """
        if item_id not in self._items:
            raise KeyError(item_id)
        del self._items[item_id]
