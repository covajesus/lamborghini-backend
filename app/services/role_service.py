import re
from uuid import uuid4

from app.domain.entities import Role
from app.domain.permissions import ALL_PERMISSION_KEYS, next_available_color
from app.schemas.admin_resources import RoleCreate, RoleUpdate

_KEY_PATTERN = re.compile(r"^[a-z][a-z0-9_-]{1,59}$")
_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")


class RoleService:
    """Role CRUD with unique colors and permission validation."""

    def __init__(self, repository) -> None:
        """
        @param repository: Role repository
        @return: None
        """
        self._repository = repository

    def list_roles(self) -> list[Role]:
        """
        @return: All roles
        """
        return self._repository.list()

    def get_role(self, role_id: str) -> Role | None:
        """
        @param role_id: Role id
        @return: Role or None
        """
        return self._repository.get_by_id(role_id)

    def create_role(self, payload: RoleCreate) -> Role:
        """
        @param payload: Create DTO
        @return: Created role
        """
        key = self._normalize_key(payload.key)
        self._ensure_unique_key(key)
        color = self._resolve_color(payload.color)
        permissions = self._sanitize_permissions(payload.permissions)
        entity = Role(
            id=payload.id or str(uuid4()),
            key=key,
            name=payload.name.strip(),
            description=(payload.description or "").strip(),
            color=color,
            permissions=permissions,
            is_system=False,
            active=bool(payload.active),
        )
        return self._repository.create(entity)

    def update_role(self, role_id: str, payload: RoleUpdate) -> Role:
        """
        @param role_id: Role id
        @param payload: Update DTO
        @return: Updated role
        """
        current = self._repository.get_by_id(role_id)
        if not current:
            raise KeyError(role_id)

        changes = payload.model_dump(exclude_unset=True)
        if "key" in changes:
            if current.is_system:
                raise ValueError("System role keys cannot be changed")
            key = self._normalize_key(str(changes["key"]))
            self._ensure_unique_key(key, exclude_id=role_id)
            changes["key"] = key
        if "name" in changes and changes["name"] is not None:
            changes["name"] = str(changes["name"]).strip()
        if "description" in changes and changes["description"] is not None:
            changes["description"] = str(changes["description"]).strip()
        if "color" in changes and changes["color"] is not None:
            changes["color"] = self._resolve_color(str(changes["color"]), exclude_id=role_id)
        if "permissions" in changes and changes["permissions"] is not None:
            changes["permissions"] = self._sanitize_permissions(changes["permissions"])
        # Prevent flipping system flag through updates.
        changes.pop("is_system", None)
        return self._repository.update(role_id, **changes)

    def delete_role(self, role_id: str) -> None:
        """
        @param role_id: Role id
        @return: None
        """
        current = self._repository.get_by_id(role_id)
        if not current:
            raise KeyError(role_id)
        if current.is_system:
            raise ValueError("System roles cannot be deleted")
        self._repository.delete(role_id)

    def _normalize_key(self, key: str) -> str:
        normalized = str(key or "").strip().lower()
        if not _KEY_PATTERN.match(normalized):
            raise ValueError("Role key must be lowercase letters, numbers, _ or -")
        return normalized

    def _ensure_unique_key(self, key: str, exclude_id: str | None = None) -> None:
        for item in self._repository.list():
            if item.key == key and item.id != exclude_id:
                raise ValueError(f"Role key already exists: {key}")

    def _resolve_color(self, color: str | None, exclude_id: str | None = None) -> str:
        used = {
            item.color.strip().upper()
            for item in self._repository.list()
            if item.id != exclude_id
        }
        if color:
            candidate = color.strip()
            if not _COLOR_PATTERN.match(candidate):
                raise ValueError("Color must be a hex value like #B8860B")
            normalized = f"#{candidate[1:].upper()}"
            if normalized.upper() in used:
                raise ValueError("Role color must be unique")
            return normalized
        return next_available_color(used)

    def _sanitize_permissions(self, permissions: list[str] | None) -> list[str]:
        allowed = set(ALL_PERMISSION_KEYS)
        cleaned: list[str] = []
        for item in permissions or []:
            key = str(item or "").strip()
            if key in allowed and key not in cleaned:
                cleaned.append(key)
        return cleaned
