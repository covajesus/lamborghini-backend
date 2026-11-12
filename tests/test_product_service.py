import pytest

from app.domain.entities import Audience, Product
from app.repositories.product_repository import InMemoryProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.product_service import ProductService


@pytest.fixture
def service() -> ProductService:
    seed = [
        Product(
            id="p1",
            slug="cap-black",
            name="Black Cap",
            audience=Audience.ACCESSORIES,
            group="Head",
            type="Cap",
            line="caps",
            price=99000,
            description="Premium black cap",
            composition="Microfiber",
            care="Wipe clean",
            image="/media/cap.jpg",
            colors=["Black"],
            sizes=["One"],
            featured=True,
        )
    ]
    return ProductService(InMemoryProductRepository(seed))


def test_list_products_returns_seed(service: ProductService) -> None:
    items = service.list_products()
    assert len(items) == 1
    assert items[0].slug == "cap-black"


def test_create_and_update_product(service: ProductService) -> None:
    created = service.create_product(
        ProductCreate(
            slug="sneaker-navy",
            name="Navy Sneaker",
            audience=Audience.MEN,
            group="Footwear",
            type="Sneakers",
            line="footwear",
            price=189000,
            description="Navy lifestyle sneaker",
            composition="Suede",
            care="Wipe dry",
            image="/media/sneaker.jpg",
            colors=["Navy"],
            sizes=["42"],
        )
    )
    assert created.id
    updated = service.update_product(created.id, ProductUpdate(price=199000, featured=True))
    assert updated.price == 199000
    assert updated.featured is True


def test_get_missing_product_raises(service: ProductService) -> None:
    with pytest.raises(KeyError):
        service.get_product("missing")
