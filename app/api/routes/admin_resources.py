from app.api.deps import get_payment_repo, get_setting_repo, get_staff_repo
from app.api.routes.crud_factory import build_crud_router
from app.domain.entities import Payment, Setting, StaffUser
from app.schemas.admin_resources import (
    PaymentCreate,
    PaymentRead,
    PaymentUpdate,
    SettingCreate,
    SettingRead,
    SettingUpdate,
    StaffUserCreate,
    StaffUserRead,
    StaffUserUpdate,
)

payments_router = build_crud_router(
    prefix="/payments",
    tags=["payments"],
    entity_cls=Payment,
    create_schema=PaymentCreate,
    update_schema=PaymentUpdate,
    read_schema=PaymentRead,
    get_repo=get_payment_repo,
)

users_router = build_crud_router(
    prefix="/users",
    tags=["users"],
    entity_cls=StaffUser,
    create_schema=StaffUserCreate,
    update_schema=StaffUserUpdate,
    read_schema=StaffUserRead,
    get_repo=get_staff_repo,
)

settings_router = build_crud_router(
    prefix="/settings",
    tags=["settings"],
    entity_cls=Setting,
    create_schema=SettingCreate,
    update_schema=SettingUpdate,
    read_schema=SettingRead,
    get_repo=get_setting_repo,
)
