from copy import deepcopy

from app.domain.entities import AdminUser


class InMemoryUserRepository:
    def __init__(self, seed: list[AdminUser] | None = None) -> None:
        self._items: dict[str, AdminUser] = {}
        for user in seed or []:
            self._items[user.id] = deepcopy(user)

    def get_by_email(self, email: str) -> AdminUser | None:
        needle = email.lower()
        for user in self._items.values():
            if user.email.lower() == needle:
                return deepcopy(user)
        return None

    def get_by_id(self, user_id: str) -> AdminUser | None:
        user = self._items.get(user_id)
        return deepcopy(user) if user else None
