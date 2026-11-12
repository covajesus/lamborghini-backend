from dataclasses import dataclass, field
from enum import StrEnum


class Audience(StrEnum):
    MEN = "men"
    WOMEN = "women"
    ACCESSORIES = "accessories"


@dataclass(slots=True)
class Product:
    """
    Sellable catalog item.

    Prices are stored as integer CLP without decimals.
    """

    id: str
    slug: str
    name: str
    audience: Audience
    group: str
    type: str
    line: str
    price: int
    description: str
    composition: str
    care: str
    image: str
    images: list[str] = field(default_factory=list)
    colors: list[str] = field(default_factory=list)
    sizes: list[str] = field(default_factory=list)
    options: list[dict] = field(default_factory=list)
    color_images: dict[str, list[str]] = field(default_factory=dict)
    variants: list[dict] = field(default_factory=list)
    featured: bool = False
    compare_at: int | None = None
    active: bool = True


@dataclass(slots=True)
class AdminUser:
    """Back-office user authenticated through JWT-protected routes."""

    id: str
    email: str
    full_name: str
    hashed_password: str
    role: str = "admin"


@dataclass(slots=True)
class InventoryItem:
    """Stock row linked to a catalog product."""

    id: str
    product_id: str
    sku: str
    warehouse: str
    quantity: int
    reserved: int = 0
    average_cost: float = 0.0
    active: bool = True


@dataclass(slots=True)
class Payment:
    """Payment / order settlement record."""

    id: str
    reference: str
    customer_name: str
    amount: int
    method: str
    status: str
    paid_at: str
    active: bool = True


@dataclass(slots=True)
class StaffUser:
    """Operative user managed from the admin Users module."""

    id: str
    full_name: str
    email: str
    role: str
    phone: str = ""
    active: bool = True


@dataclass(slots=True)
class Role:
    """Admin role with dynamic permissions and a unique badge color."""

    id: str
    key: str
    name: str
    description: str
    color: str
    permissions: list[str]
    is_system: bool = False
    active: bool = True


@dataclass(slots=True)
class Setting:
    """Key/value configuration entry for the storefront/admin."""

    id: str
    key: str
    label: str
    value: str
    group: str = "general"
    active: bool = True


@dataclass(slots=True)
class Slide:
    """Home hero carousel slide managed from the admin."""

    id: str
    sort_order: int
    kicker: str
    title: str
    text: str
    cta_label: str
    cta_to: str
    image: str
    image_position: str = "center center"
    active: bool = True


@dataclass(slots=True)
class Category:
    """Shop category shown on the storefront and used by products."""

    id: str
    slug: str
    name: str
    line: str
    image: str
    sort_order: int = 0
    active: bool = True
