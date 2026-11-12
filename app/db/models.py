from sqlalchemy import Boolean, Float, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    audience: Mapped[str] = mapped_column(String(40))
    group_name: Mapped[str] = mapped_column("group", String(80))
    type: Mapped[str] = mapped_column(String(80))
    line: Mapped[str] = mapped_column(String(80))
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(Text)
    composition: Mapped[str] = mapped_column(String(255))
    care: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(String(255))
    images: Mapped[list] = mapped_column(JSON, default=list)
    colors: Mapped[list] = mapped_column(JSON, default=list)
    sizes: Mapped[list] = mapped_column(JSON, default=list)
    options: Mapped[list] = mapped_column(JSON, default=list)
    color_images: Mapped[dict] = mapped_column(JSON, default=dict)
    variants: Mapped[list] = mapped_column(JSON, default=list)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    compare_at: Mapped[int | None] = mapped_column(Integer, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class AdminUserModel(Base):
    __tablename__ = "admin_users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(160))
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(40), default="admin")


class InventoryItemModel(Base):
    __tablename__ = "inventory_items"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    product_id: Mapped[str] = mapped_column(String(64), index=True)
    sku: Mapped[str] = mapped_column(String(80), index=True)
    warehouse: Mapped[str] = mapped_column(String(120))
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    reserved: Mapped[int] = mapped_column(Integer, default=0)
    average_cost: Mapped[float] = mapped_column(Float, default=0.0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class PaymentModel(Base):
    __tablename__ = "payments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    reference: Mapped[str] = mapped_column(String(80), index=True)
    customer_name: Mapped[str] = mapped_column(String(160))
    amount: Mapped[int] = mapped_column(Integer)
    method: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(40))
    paid_at: Mapped[str] = mapped_column(String(40))
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class StaffUserModel(Base):
    __tablename__ = "staff_users"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(160))
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    role: Mapped[str] = mapped_column(String(40))
    phone: Mapped[str] = mapped_column(String(60), default="")
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class RoleModel(Base):
    __tablename__ = "roles"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    key: Mapped[str] = mapped_column(String(60), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(String(255), default="")
    color: Mapped[str] = mapped_column(String(20), unique=True)
    permissions: Mapped[list] = mapped_column(JSON, default=list)
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class SettingModel(Base):
    __tablename__ = "settings"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    key: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    label: Mapped[str] = mapped_column(String(160))
    value: Mapped[str] = mapped_column(Text)
    group_name: Mapped[str] = mapped_column("group", String(80), default="general")
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class SlideModel(Base):
    __tablename__ = "slides"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, index=True)
    kicker: Mapped[str] = mapped_column(String(120))
    title: Mapped[str] = mapped_column(String(200))
    text: Mapped[str] = mapped_column(Text)
    cta_label: Mapped[str] = mapped_column(String(80))
    cta_to: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(String(255))
    image_position: Mapped[str] = mapped_column(String(80), default="center center")
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    line: Mapped[str] = mapped_column(String(255))
    image: Mapped[str] = mapped_column(String(255))
    sort_order: Mapped[int] = mapped_column(Integer, default=0, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
