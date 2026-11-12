from uuid import uuid4

from app.domain.entities import Audience, Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.services.product_variants import ensure_variant_structure, normalize_product_payload


class ProductService:
    """Application service for catalog reads and admin mutations."""

    def __init__(self, repository) -> None:
        """
        Create a product service.

        @param repository: Product repository implementation
        @return: None
        """
        self._repository = repository

    def list_products(self, audience: Audience | None = None, *, include_inactive: bool = False) -> list[Product]:
        """
        List products with optional audience filter.

        @param audience: Audience segment filter or None for all
        @param include_inactive: When True, include inactive products
        @return: List of Product entities
        """
        return self._repository.list(audience=audience, active_only=not include_inactive)

    def get_product(self, product_id: str) -> Product:
        """
        Get one product by id.

        @param product_id: Product identifier
        @return: Product entity
        """
        product = self._repository.get_by_id(product_id)
        if not product:
            raise KeyError(product_id)
        return product

    def get_by_slug(self, slug: str) -> Product:
        """
        Get one product by SEO slug.

        @param slug: Product slug
        @return: Product entity
        """
        product = self._repository.get_by_slug(slug)
        if not product:
            raise KeyError(slug)
        return product

    def create_product(self, payload: ProductCreate) -> Product:
        """
        Create and persist a new product.

        @param payload: Product create DTO
        @return: Created Product entity
        """
        normalized = normalize_product_payload(
            options=[item.model_dump() for item in payload.options],
            variants=[item.model_dump() for item in payload.variants],
            color_images=payload.color_images,
            colors=payload.colors,
            sizes=payload.sizes,
            image=payload.image,
            images=payload.images,
        )
        product = Product(
            id=payload.id or str(uuid4()),
            slug=payload.slug,
            name=payload.name,
            audience=payload.audience,
            group=payload.group,
            type=payload.type,
            line=payload.line,
            price=payload.price,
            description=payload.description,
            composition=payload.composition,
            care=payload.care,
            featured=payload.featured,
            compare_at=payload.compare_at,
            active=payload.active,
            **normalized,
        )
        return self._repository.create(ensure_variant_structure(product))

    def update_product(self, product_id: str, payload: ProductUpdate) -> Product:
        """
        Apply a partial update to an existing product.

        @param product_id: Product identifier
        @param payload: Product update DTO
        @return: Updated Product entity
        """
        changes = payload.model_dump(exclude_unset=True)
        media_keys = ("options", "variants", "color_images", "colors", "sizes", "image", "images")
        if any(key in changes for key in media_keys):
            current = self.get_product(product_id)
            normalized = normalize_product_payload(
                options=changes.get("options", current.options),
                variants=changes.get("variants", current.variants),
                color_images=changes.get("color_images", current.color_images),
                colors=changes.get("colors", current.colors),
                sizes=changes.get("sizes", current.sizes),
                image=changes.get("image", current.image),
                images=changes.get("images", current.images),
            )
            changes.update(normalized)
        return self._repository.update(product_id, **changes)

    def delete_product(self, product_id: str) -> None:
        """
        Delete a product by id.

        @param product_id: Product identifier
        @return: None
        """
        self._repository.delete(product_id)
