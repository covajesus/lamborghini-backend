from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_admin, get_roles_repo
from app.domain.permissions import PERMISSION_CATALOG
from app.schemas.admin_resources import PermissionRead, RoleCreate, RoleRead, RoleUpdate
from app.services.role_service import RoleService

router = APIRouter(prefix="/roles", tags=["roles"])


def get_role_service(repo=Depends(get_roles_repo)) -> RoleService:
    """
    @param repo: Roles repository
    @return: Role service
    """
    return RoleService(repo)


@router.get("/permissions", response_model=list[PermissionRead])
def list_permissions(_: object = Depends(get_current_admin)):
    return [
        PermissionRead(key=item.key, label=item.label, group=item.group)
        for item in PERMISSION_CATALOG
    ]


@router.get("", response_model=list[RoleRead])
def list_roles(
    service: RoleService = Depends(get_role_service),
    _: object = Depends(get_current_admin),
):
    return [RoleRead.model_validate(item, from_attributes=True) for item in service.list_roles()]


@router.get("/{item_id}", response_model=RoleRead)
def get_role(
    item_id: str,
    service: RoleService = Depends(get_role_service),
    _: object = Depends(get_current_admin),
):
    item = service.get_role(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return RoleRead.model_validate(item, from_attributes=True)


@router.post("", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(
    payload: RoleCreate,
    service: RoleService = Depends(get_role_service),
    _: object = Depends(get_current_admin),
):
    try:
        created = service.create_role(payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return RoleRead.model_validate(created, from_attributes=True)


@router.patch("/{item_id}", response_model=RoleRead)
def update_role(
    item_id: str,
    payload: RoleUpdate,
    service: RoleService = Depends(get_role_service),
    _: object = Depends(get_current_admin),
):
    try:
        updated = service.update_role(item_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return RoleRead.model_validate(updated, from_attributes=True)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    item_id: str,
    service: RoleService = Depends(get_role_service),
    _: object = Depends(get_current_admin),
):
    try:
        service.delete_role(item_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
