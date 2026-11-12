from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.db.mappers import product_to_entity, product_to_model
from app.db.models import ProductModel
from app.domain.entities import Audience, Product


class SqlProductRepository:
    """MySQL-backed product repository."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        """
        @param session_factory: SQLAlchemy session factory
        @return: None
        """
        self._session_factory = session_factory

    def list(
        self,
        *,
        audience: Audience | None = None,
        active_only: bool = True,
    ) -> list[Product]:
        """
        @param audience: Audience segment filter or None for all
        @param active_only: When True, exclude inactive products
        @return: Sorted list of Product entities
        """
        with self._session_factory() as session:
            stmt = select(ProductModel)
            if active_only:
                stmt = stmt.where(ProductModel.active.is_(True))
            if audience:
                stmt = stmt.where(ProductModel.audience == audience.value)
            stmt = stmt.order_by(ProductModel.name.asc())
            return [product_to_entity(row) for row in session.scalars(stmt).all()]

    def get_by_id(self, product_id: str) -> Product | None:
        """
        @param product_id: Product identifier
        @return: Product entity or None
        """
        with self._session_factory() as session:
            row = session.get(ProductModel, product_id)
            return product_to_entity(row) if row else None

    def get_by_slug(self, slug: str) -> Product | None:
        """
        @param slug: Product slug
        @return: Product entity or None
        """
        with self._session_factory() as session:
            row = session.scalar(select(ProductModel).where(ProductModel.slug == slug))
            return product_to_entity(row) if row else None

    def create(self, product: Product) -> Product:
        """
        @param product: Product entity to store
        @return: Stored Product entity
        """
        with self._session_factory() as session:
            if session.get(ProductModel, product.id):
                raise ValueError(f"Product id already exists: {product.id}")
            row = product_to_model(product)
            session.add(row)
            session.commit()
            session.refresh(row)
            return product_to_entity(row)

    def update(self, product_id: str, **changes) -> Product:
        """
        @param product_id: Product identifier
        @param changes: Field names and values to apply
        @return: Updated Product entity
        """
        with self._session_factory() as session:
            row = session.get(ProductModel, product_id)
            if not row:
                raise KeyError(product_id)
            field_map = {
                "group": "group_name",
                "audience": "audience",
            }
            for key, value in changes.items():
                if value is None and key != "compare_at":
                    continue
                attr = field_map.get(key, key)
                if key == "audience" and isinstance(value, Audience):
                    value = value.value
                if hasattr(row, attr):
                    setattr(row, attr, value)
            session.commit()
            session.refresh(row)
            return product_to_entity(row)

    def delete(self, product_id: str) -> None:
        """
        @param product_id: Product identifier
        @return: None
        """
        with self._session_factory() as session:
            row = session.get(ProductModel, product_id)
            if not row:
                raise KeyError(product_id)
            session.delete(row)
            session.commit()
