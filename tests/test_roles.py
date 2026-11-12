from fastapi.testclient import TestClient

from app.api.deps import configure_repositories
from app.core.config import get_settings
from app.core.security import hash_password
from app.data.seed import seed_products
from app.data.seed_admin_resources import (
    seed_categories,
    seed_inventory,
    seed_payments,
    seed_roles,
    seed_settings,
    seed_slides,
    seed_staff_users,
)
from app.domain.entities import AdminUser
from app.domain.permissions import next_available_color
from app.main import create_app
from app.repositories.memory_repository import InMemoryRepository
from app.repositories.product_repository import InMemoryProductRepository
from app.repositories.user_repository import InMemoryUserRepository


def build_client() -> TestClient:
    settings = get_settings()
    configure_repositories(
        InMemoryProductRepository(seed_products()),
        InMemoryUserRepository(
            [
                AdminUser(
                    id="admin-1",
                    email=settings.admin_email,
                    full_name="Store Admin",
                    hashed_password=hash_password(settings.admin_password),
                )
            ]
        ),
        inventory=InMemoryRepository(seed_inventory()),
        payments=InMemoryRepository(seed_payments()),
        staff_users=InMemoryRepository(seed_staff_users()),
        settings=InMemoryRepository(seed_settings()),
        slides=InMemoryRepository(seed_slides()),
        categories=InMemoryRepository(seed_categories()),
        roles=InMemoryRepository(seed_roles()),
    )
    return TestClient(create_app())


def auth_headers(client: TestClient) -> dict[str, str]:
    settings = get_settings()
    login = client.post(
        "/api/v1/auth/login",
        json={"email": settings.admin_email, "password": settings.admin_password},
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_seed_roles_have_unique_colors() -> None:
    colors = [item.color.upper() for item in seed_roles()]
    assert len(colors) == len(set(colors))


def test_next_available_color_skips_used() -> None:
    assert next_available_color({"#B8860B", "#2F5D50"}) == "#5B6B7A"


def test_list_default_roles_and_permissions() -> None:
    client = build_client()
    headers = auth_headers(client)
    roles = client.get("/api/v1/roles", headers=headers)
    assert roles.status_code == 200
    payload = roles.json()
    assert len(payload) >= 3
    keys = {item["key"] for item in payload}
    assert {"admin", "editor", "viewer"} <= keys

    permissions = client.get("/api/v1/roles/permissions", headers=headers)
    assert permissions.status_code == 200
    assert len(permissions.json()) >= 10


def test_create_role_gets_unique_color_and_cannot_delete_system() -> None:
    client = build_client()
    headers = auth_headers(client)
    created = client.post(
        "/api/v1/roles",
        headers=headers,
        json={
            "key": "ops",
            "name": "Operaciones",
            "description": "Gestiona inventario y pagos.",
            "permissions": ["inventory.read", "inventory.write", "payments.read"],
        },
    )
    assert created.status_code == 201
    body = created.json()
    assert body["color"]
    assert body["color"].upper() not in {"#B8860B", "#2F5D50", "#5B6B7A"}

    system = next(item for item in client.get("/api/v1/roles", headers=headers).json() if item["key"] == "admin")
    deleted = client.delete(f"/api/v1/roles/{system['id']}", headers=headers)
    assert deleted.status_code == 400
