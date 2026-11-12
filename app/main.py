from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.deps import configure_repositories
from app.api.router import api_router
from app.core.config import get_settings
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
from app.db.bootstrap import seed_database_if_empty
from app.db.mappers import (
    category_to_entity,
    category_to_model,
    inventory_to_entity,
    inventory_to_model,
    payment_to_entity,
    payment_to_model,
    role_to_entity,
    role_to_model,
    setting_to_entity,
    setting_to_model,
    slide_to_entity,
    slide_to_model,
    staff_to_entity,
    staff_to_model,
)
from app.db.models import (
    CategoryModel,
    InventoryItemModel,
    PaymentModel,
    RoleModel,
    SettingModel,
    SlideModel,
    StaffUserModel,
)
from app.db.session import get_session_factory
from app.repositories.memory_repository import InMemoryRepository
from app.repositories.product_repository import InMemoryProductRepository
from app.repositories.sql_product_repository import SqlProductRepository
from app.repositories.sql_resource_repository import SqlResourceRepository
from app.repositories.sql_user_repository import SqlUserRepository
from app.repositories.user_repository import InMemoryUserRepository

UPLOAD_ROOT = Path(__file__).resolve().parents[1] / "uploads"


def _configure_memory() -> None:
    """
    Wire in-memory repositories (tests / fallback).

    @return: None
    """
    configure_repositories(
        InMemoryProductRepository(seed_products()),
        InMemoryUserRepository([seed_admin()]),
        inventory=InMemoryRepository(seed_inventory()),
        payments=InMemoryRepository(seed_payments()),
        staff_users=InMemoryRepository(seed_staff_users()),
        settings=InMemoryRepository(seed_settings()),
        slides=InMemoryRepository(seed_slides()),
        categories=InMemoryRepository(seed_categories()),
        roles=InMemoryRepository(seed_roles()),
    )


def _configure_sql() -> None:
    """
    Wire MySQL repositories and seed empty tables.

    @return: None
    """
    session_factory = get_session_factory()
    seed_database_if_empty(session_factory)
    configure_repositories(
        SqlProductRepository(session_factory),
        SqlUserRepository(session_factory),
        inventory=SqlResourceRepository(
            session_factory,
            InventoryItemModel,
            inventory_to_entity,
            inventory_to_model,
        ),
        payments=SqlResourceRepository(
            session_factory,
            PaymentModel,
            payment_to_entity,
            payment_to_model,
        ),
        staff_users=SqlResourceRepository(
            session_factory,
            StaffUserModel,
            staff_to_entity,
            staff_to_model,
        ),
        settings=SqlResourceRepository(
            session_factory,
            SettingModel,
            setting_to_entity,
            setting_to_model,
            field_map={"group": "group_name"},
        ),
        slides=SqlResourceRepository(
            session_factory,
            SlideModel,
            slide_to_entity,
            slide_to_model,
        ),
        categories=SqlResourceRepository(
            session_factory,
            CategoryModel,
            category_to_entity,
            category_to_model,
        ),
        roles=SqlResourceRepository(
            session_factory,
            RoleModel,
            role_to_entity,
            role_to_model,
        ),
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Application lifespan hook.

    @param _: FastAPI application instance (unused)
    @return: Async context manager for startup and shutdown
    """
    settings = get_settings()
    if settings.persistence == "memory":
        _configure_memory()
    else:
        _configure_sql()
    yield


def create_app() -> FastAPI:
    """
    Build and configure the FastAPI application.

    @return: Configured FastAPI ASGI application
    """
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.api_prefix)
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    app.mount("/media/uploads", StaticFiles(directory=str(UPLOAD_ROOT)), name="uploads")
    return app


app = create_app()
