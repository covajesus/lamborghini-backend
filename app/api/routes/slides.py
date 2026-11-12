from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials

from app.api.deps import bearer, get_current_admin, get_slides_repo
from app.core.security import decode_access_token
from app.domain.entities import Slide
from app.schemas.slide import SlideCreate, SlideRead, SlideUpdate

router = APIRouter(prefix="/slides", tags=["slides"])


def _sorted(items: list[Slide]) -> list[Slide]:
    return sorted(items, key=lambda item: (item.sort_order, item.id))


def to_read(item: Slide) -> SlideRead:
    """
    @param item: Domain Slide
    @return: SlideRead DTO
    """
    return SlideRead.model_validate(item, from_attributes=True)


def _is_admin_token(credentials: HTTPAuthorizationCredentials | None) -> bool:
    if credentials is None:
        return False
    try:
        decode_access_token(credentials.credentials)
        return True
    except ValueError:
        return False


@router.get("", response_model=list[SlideRead])
def list_slides(
    include_inactive: bool = Query(default=False),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    repo=Depends(get_slides_repo),
) -> list[SlideRead]:
    """
    Public list returns active slides. Authenticated admin can include inactive.
    """
    show_all = include_inactive and _is_admin_token(credentials)
    items = repo.list() if show_all else repo.list(active_only=True)
    return [to_read(item) for item in _sorted(items)]


@router.get("/{slide_id}", response_model=SlideRead)
def get_slide(slide_id: str, repo=Depends(get_slides_repo)) -> SlideRead:
    item = repo.get_by_id(slide_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slide not found")
    return to_read(item)


@router.post("", response_model=SlideRead, status_code=status.HTTP_201_CREATED)
def create_slide(
    payload: SlideCreate,
    _: object = Depends(get_current_admin),
    repo=Depends(get_slides_repo),
) -> SlideRead:
    data = payload.model_dump()
    data["id"] = data.get("id") or None
    try:
        created = repo.create(Slide(**{**data, "id": data["id"] or ""}))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return to_read(created)


@router.patch("/{slide_id}", response_model=SlideRead)
def update_slide(
    slide_id: str,
    payload: SlideUpdate,
    _: object = Depends(get_current_admin),
    repo=Depends(get_slides_repo),
) -> SlideRead:
    try:
        updated = repo.update(slide_id, **payload.model_dump(exclude_unset=True))
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slide not found") from exc
    return to_read(updated)


@router.delete("/{slide_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slide(
    slide_id: str,
    _: object = Depends(get_current_admin),
    repo=Depends(get_slides_repo),
) -> None:
    try:
        repo.delete(slide_id)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slide not found") from exc
