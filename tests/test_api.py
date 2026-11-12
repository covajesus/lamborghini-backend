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


def test_health() -> None:
    client = build_client()
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_products_public() -> None:
    client = build_client()
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_list_slides_public() -> None:
    client = build_client()
    response = client.get("/api/v1/slides")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 1
    assert payload[0]["cta_label"]
    assert payload[0]["image"]


def test_admin_create_slide() -> None:
    client = build_client()
    settings = get_settings()
    login = client.post(
        "/api/v1/auth/login",
        json={"email": settings.admin_email, "password": settings.admin_password},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    created = client.post(
        "/api/v1/slides",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "sort_order": 99,
            "kicker": "Lamborghini",
            "title": "NUEVO\nSLIDE",
            "text": "Slide de prueba",
            "cta_label": "Descubrir",
            "cta_to": "/offers",
            "image": "/media/slider-1.jpg",
            "image_position": "center center",
        },
    )
    assert created.status_code == 201
    assert created.json()["title"] == "NUEVO\nSLIDE"


def test_list_storefront_settings_public() -> None:
    client = build_client()
    response = client.get("/api/v1/storefront/settings")
    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    keys = {item["key"] for item in payload}
    assert "store_name" in keys
    assert "social_instagram" in keys


def test_list_categories_public() -> None:
    client = build_client()
    response = client.get("/api/v1/categories")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 1
    assert payload[0]["slug"]
    assert payload[0]["image"]


def test_admin_create_category() -> None:
    client = build_client()
    settings = get_settings()
    login = client.post(
        "/api/v1/auth/login",
        json={"email": settings.admin_email, "password": settings.admin_password},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    created = client.post(
        "/api/v1/categories",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "slug": "kids",
            "name": "Niños",
            "line": "Categoría de prueba",
            "image": "/media/products/prod-cap-black.jpg",
            "sort_order": 10,
            "active": True,
        },
    )
    assert created.status_code == 201
    assert created.json()["slug"] == "kids"


def test_admin_upload_image() -> None:
    client = build_client()
    settings = get_settings()
    login = client.post(
        "/api/v1/auth/login",
        json={"email": settings.admin_email, "password": settings.admin_password},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    uploaded = client.post(
        "/api/v1/uploads/image?folder=categories",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("cat.png", b"\x89PNG\r\n\x1a\nfake", "image/png")},
    )
    assert uploaded.status_code == 200
    assert uploaded.json()["url"].startswith("/media/uploads/categories/")


def test_admin_login_and_create_product() -> None:
    client = build_client()
    settings = get_settings()
    login = client.post(
        "/api/v1/auth/login",
        json={"email": settings.admin_email, "password": settings.admin_password},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    created = client.post(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "slug": "test-cap",
            "name": "Test Cap",
            "audience": "accessories",
            "group": "Cabeza",
            "type": "Gorra",
            "line": "caps",
            "price": 50000,
            "description": "Test product",
            "composition": "Cotton",
            "care": "Hand wash",
            "image": "/media/test.jpg",
            "colors": ["Negro"],
            "sizes": ["Única"],
        },
    )
    assert created.status_code == 201
    assert created.json()["slug"] == "test-cap"
