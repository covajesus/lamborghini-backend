from copy import deepcopy
from dataclasses import replace

from app.domain.entities import Audience, Product


class InMemoryProductRepository:
    """In-memory product repository (replace with SQL adapter later)."""

    def __init__(self, seed: list[Product] | None = None) -> None:
        """
        Initialize the repository with optional seed data.

        @param seed: Initial list of Product entities
        @return: None
        """
        self._items: dict[str, Product] = {}
        for product in seed or []:
            self._items[product.id] = deepcopy(product)

    def list(
        self,
        *,
        audience: Audience | None = None,
        active_only: bool = True,
    ) -> list[Product]:
        """
        List products with optional filters.

        @param audience: Audience segment filter or None for all
        @param active_only: When True, exclude inactive products
        @return: Sorted list of Product entities
        """
        items = list(self._items.values())
        if active_only:
            items = [item for item in items if item.active]
        if audience:
            items = [item for item in items if item.audience == audience]
        return sorted(items, key=lambda item: item.name)

    def get_by_id(self, product_id: str) -> Product | None:
        """
        Find a product by id.

        @param product_id: Product identifier
        @return: Product entity or None
        """
        product = self._items.get(product_id)
        return deepcopy(product) if product else None

    def get_by_slug(self, slug: str) -> Product | None:
        """
        Find a product by slug.

        @param slug: Product slug
        @return: Product entity or None
        """
        for product in self._items.values():
            if product.slug == slug:
                return deepcopy(product)
        return None

    def create(self, product: Product) -> Product:
        """
        Persist a new product.

        @param product: Product entity to store
        @return: Stored Product entity copy
        """
        if product.id in self._items:
            raise ValueError(f"Product id already exists: {product.id}")
        self._items[product.id] = deepcopy(product)
        return deepcopy(product)

    def update(self, product_id: str, **changes) -> Product:
        """
        Update fields of an existing product.

        @param product_id: Product identifier
        @param changes: Field names and values to apply
        @return: Updated Product entity copy
        """
        current = self._items.get(product_id)
        if not current:
            raise KeyError(product_id)
        payload = {key: value for key, value in changes.items() if value is not None}
        updated = replace(current, **payload)
        self._items[product_id] = updated
        return deepcopy(updated)

    def delete(self, product_id: str) -> None:
        """
        Remove a product by id.

        @param product_id: Product identifier
        @return: None
        """
        if product_id not in self._items:
            raise KeyError(product_id)
        del self._items[product_id]
