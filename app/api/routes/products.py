from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps import get_current_admin, get_product_service
from app.domain.entities import Audience, Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def to_read(product: Product) -> ProductRead:
    """
    Map a domain Product to the API response schema.

    @param product: Domain Product entity
    @return: ProductRead response DTO
    """
    return ProductRead.model_validate(product, from_attributes=True)


@router.get("", response_model=list[ProductRead])
def list_products(
    audience: Audience | None = Query(default=None),
    include_inactive: bool = Query(default=False),
    service: ProductService = Depends(get_product_service),
) -> list[ProductRead]:
    return [to_read(item) for item in service.list_products(audience, include_inactive=include_inactive)]


@router.get("/by-slug/{slug}", response_model=ProductRead)
def get_by_slug(slug: str, service: ProductService = Depends(get_product_service)) -> ProductRead:
    try:
        return to_read(service.get_by_slug(slug))
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found") from exc


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: str, service: ProductService = Depends(get_product_service)) -> ProductRead:
    try:
        return to_read(service.get_product(product_id))
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found") from exc


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    _: object = Depends(get_current_admin),
    service: ProductService = Depends(get_product_service),
) -> ProductRead:
    try:
        return to_read(service.create_product(payload))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: str,
    payload: ProductUpdate,
    _: object = Depends(get_current_admin),
    service: ProductService = Depends(get_product_service),
) -> ProductRead:
    try:
        return to_read(service.update_product(product_id, payload))
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found") from exc


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str,
    _: object = Depends(get_current_admin),
    service: ProductService = Depends(get_product_service),
) -> None:
    try:
        service.delete_product(product_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found") from exc
