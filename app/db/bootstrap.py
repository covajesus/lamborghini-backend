from sqlalchemy import func, select
from sqlalchemy.orm import Session, sessionmaker

from app.data.seed import seed_admin, seed_products
from app.data.seed_admin_resources import (
    seed_categories,
    seed_inventory,
    seed_payments,
    seed_roles,
    seed_settings,
    seed_slides,
    seed_staff_users,
)
from app.db.mappers import (
    admin_to_model,
    category_to_model,
    inventory_to_model,
    payment_to_model,
    product_to_model,
    role_to_model,
    setting_to_model,
    slide_to_model,
    staff_to_model,
)
from app.db.models import (
    AdminUserModel,
    CategoryModel,
    InventoryItemModel,
    PaymentModel,
    ProductModel,
    RoleModel,
    SettingModel,
    SlideModel,
    StaffUserModel,
)


def seed_database_if_empty(session_factory: sessionmaker[Session]) -> None:
    """
    Insert default catalog/admin data when tables are empty.

    @param session_factory: SQLAlchemy session factory
    @return: None
    """
    with session_factory() as session:
        existing_product_ids = set(session.scalars(select(ProductModel.id)).all())
        for item in seed_products():
            if item.id not in existing_product_ids:
                session.add(product_to_model(item))

        admin_count = session.scalar(select(func.count()).select_from(AdminUserModel)) or 0
        if admin_count == 0:
            session.add(admin_to_model(seed_admin()))

        inventory_count = session.scalar(select(func.count()).select_from(InventoryItemModel)) or 0
        if inventory_count == 0:
            session.add_all([inventory_to_model(item) for item in seed_inventory()])

        payment_count = session.scalar(select(func.count()).select_from(PaymentModel)) or 0
        if payment_count == 0:
            session.add_all([payment_to_model(item) for item in seed_payments()])

        staff_count = session.scalar(select(func.count()).select_from(StaffUserModel)) or 0
        if staff_count == 0:
            session.add_all([staff_to_model(item) for item in seed_staff_users()])

        existing_setting_ids = set(session.scalars(select(SettingModel.id)).all())
        for item in seed_settings():
            if item.id not in existing_setting_ids:
                session.add(setting_to_model(item))

        slide_count = session.scalar(select(func.count()).select_from(SlideModel)) or 0
        if slide_count == 0:
            session.add_all([slide_to_model(item) for item in seed_slides()])

        category_count = session.scalar(select(func.count()).select_from(CategoryModel)) or 0
        if category_count == 0:
            session.add_all([category_to_model(item) for item in seed_categories()])

        role_count = session.scalar(select(func.count()).select_from(RoleModel)) or 0
        if role_count == 0:
            session.add_all([role_to_model(item) for item in seed_roles()])

        session.commit()
