from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from app.api.deps import bearer, get_categories_repo, get_current_admin
from app.core.security import decode_access_token
from app.domain.entities import Category
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


def _sorted(items: list[Category]) -> list[Category]:
    return sorted(items, key=lambda item: (item.sort_order, item.name, item.id))


def to_read(item: Category) -> CategoryRead:
    """
    @param item: Domain Category
    @return: CategoryRead DTO
    """
    return CategoryRead.model_validate(item, from_attributes=True)


def _is_admin_token(credentials: HTTPAuthorizationCredentials | None) -> bool:
    if credentials is None:
        return False
    try:
        decode_access_token(credentials.credentials)
        return True
    except ValueError:
        return False


@router.get("", response_model=list[CategoryRead])
def list_categories(
    include_inactive: bool = Query(default=False),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    repo=Depends(get_categories_repo),
) -> list[CategoryRead]:
    """
    Public list returns active categories. Authenticated admin can include inactive.
    """
    show_all = include_inactive and _is_admin_token(credentials)
    items = repo.list() if show_all else repo.list(active_only=True)
    return [to_read(item) for item in _sorted(items)]


@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: str, repo=Depends(get_categories_repo)) -> CategoryRead:
    item = repo.get_by_id(category_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return to_read(item)


@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    _: object = Depends(get_current_admin),
    repo=Depends(get_categories_repo),
) -> CategoryRead:
    data = payload.model_dump()
    try:
        created = repo.create(Category(**{**data, "id": data.get("id") or ""}))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return to_read(created)


@router.patch("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: str,
    payload: CategoryUpdate,
    _: object = Depends(get_current_admin),
    repo=Depends(get_categories_repo),
) -> CategoryRead:
    try:
        updated = repo.update(category_id, **payload.model_dump(exclude_unset=True))
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found") from exc
    return to_read(updated)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str,
    _: object = Depends(get_current_admin),
    repo=Depends(get_categories_repo),
) -> None:
    try:
        repo.delete(category_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found") from exc
