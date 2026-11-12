from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_admin, get_inventory_repo
from app.schemas.admin_resources import InventoryCreate, InventoryRead, InventoryUpdate
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["inventory"])


def get_inventory_service(repo=Depends(get_inventory_repo)) -> InventoryService:
    """
    @param repo: Inventory repository
    @return: Inventory service
    """
    return InventoryService(repo)


@router.get("", response_model=list[InventoryRead])
def list_inventory(
    service: InventoryService = Depends(get_inventory_service),
    _: object = Depends(get_current_admin),
):
    return [InventoryRead.model_validate(item, from_attributes=True) for item in service.list_items()]


@router.get("/{item_id}", response_model=InventoryRead)
def get_inventory(
    item_id: str,
    service: InventoryService = Depends(get_inventory_service),
    _: object = Depends(get_current_admin),
):
    item = service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return InventoryRead.model_validate(item, from_attributes=True)


@router.post("", response_model=InventoryRead, status_code=status.HTTP_201_CREATED)
def create_inventory(
    payload: InventoryCreate,
    service: InventoryService = Depends(get_inventory_service),
    _: object = Depends(get_current_admin),
):
    data = payload.model_copy(update={"id": payload.id or str(uuid4())})
    try:
        created = service.create_item(data)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return InventoryRead.model_validate(created, from_attributes=True)


@router.patch("/{item_id}", response_model=InventoryRead)
def update_inventory(
    item_id: str,
    payload: InventoryUpdate,
    service: InventoryService = Depends(get_inventory_service),
    _: object = Depends(get_current_admin),
):
    try:
        updated = service.update_item(item_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return InventoryRead.model_validate(updated, from_attributes=True)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory(
    item_id: str,
    service: InventoryService = Depends(get_inventory_service),
    _: object = Depends(get_current_admin),
):
    try:
        service.delete_item(item_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found") from exc
