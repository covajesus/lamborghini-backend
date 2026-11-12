"""Catalog of admin permissions available for dynamic roles."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PermissionDefinition:
    """Single permission option shown in the roles form."""

    key: str
    label: str
    group: str


PERMISSION_CATALOG: tuple[PermissionDefinition, ...] = (
    PermissionDefinition("dashboard.view", "Ver inicio", "General"),
    PermissionDefinition("products.read", "Ver productos", "Productos"),
    PermissionDefinition("products.write", "Crear y editar productos", "Productos"),
    PermissionDefinition("categories.read", "Ver categorías", "Categorías"),
    PermissionDefinition("categories.write", "Crear y editar categorías", "Categorías"),
    PermissionDefinition("slides.read", "Ver slider", "Slider"),
    PermissionDefinition("slides.write", "Crear y editar diapositivas", "Slider"),
    PermissionDefinition("inventory.read", "Ver inventario", "Inventario"),
    PermissionDefinition("inventory.write", "Crear y editar inventario", "Inventario"),
    PermissionDefinition("payments.read", "Ver pagos", "Pagos"),
    PermissionDefinition("payments.write", "Crear y editar pagos", "Pagos"),
    PermissionDefinition("users.read", "Ver usuarios", "Usuarios"),
    PermissionDefinition("users.write", "Crear y editar usuarios", "Usuarios"),
    PermissionDefinition("roles.read", "Ver roles", "Roles"),
    PermissionDefinition("roles.write", "Crear y editar roles", "Roles"),
    PermissionDefinition("settings.read", "Ver configuraciones", "Configuraciones"),
    PermissionDefinition("settings.write", "Editar configuraciones", "Configuraciones"),
)

ALL_PERMISSION_KEYS: tuple[str, ...] = tuple(item.key for item in PERMISSION_CATALOG)

# Unique palette — each role must use a different color.
ROLE_COLOR_PALETTE: tuple[str, ...] = (
    "#B8860B",
    "#2F5D50",
    "#5B6B7A",
    "#8B3A3A",
    "#3D5A80",
    "#6B4F2A",
    "#4A6741",
    "#7A5C8F",
    "#A65D2E",
    "#2C6E6A",
    "#6E4C63",
    "#4F5D75",
)


def next_available_color(used_colors: set[str]) -> str:
    """
    Pick the first palette color not already assigned.

    @param used_colors: Colors already in use (case-insensitive)
    @return: Hex color string
    """
    normalized = {color.strip().upper() for color in used_colors}
    for color in ROLE_COLOR_PALETTE:
        if color.upper() not in normalized:
            return color
    raise ValueError("No available role colors left in the palette")
