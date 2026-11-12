from typing import Any, Callable, Type
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.api.deps import get_current_admin
from app.repositories.memory_repository import InMemoryRepository


def build_crud_router(
    *,
    prefix: str,
    tags: list[str],
    entity_cls: Type[Any],
    create_schema: Type[BaseModel],
    update_schema: Type[BaseModel],
    read_schema: Type[BaseModel],
    get_repo: Callable[[], InMemoryRepository],
) -> APIRouter:
    """
    Build a standard admin CRUD router for an in-memory resource.

    @param prefix: URL prefix
    @param tags: OpenAPI tags
    @param entity_cls: Domain dataclass type
    @param create_schema: Create DTO type
    @param update_schema: Update DTO type
    @param read_schema: Read DTO type
    @param get_repo: Callable returning the repository
    @return: Configured APIRouter
    """
    router = APIRouter(prefix=prefix, tags=tags)

    @router.get("", response_model=list[read_schema])
    def list_items(repo: InMemoryRepository = Depends(get_repo), _: object = Depends(get_current_admin)):
        return [read_schema.model_validate(item, from_attributes=True) for item in repo.list()]

    @router.get("/{item_id}", response_model=read_schema)
    def get_item(item_id: str, repo: InMemoryRepository = Depends(get_repo), _: object = Depends(get_current_admin)):
        item = repo.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return read_schema.model_validate(item, from_attributes=True)

    @router.post("", response_model=read_schema, status_code=status.HTTP_201_CREATED)
    def create_item(
        payload: create_schema,
        repo: InMemoryRepository = Depends(get_repo),
        _: object = Depends(get_current_admin),
    ):
        data = payload.model_dump()
        data["id"] = data.get("id") or str(uuid4())
        try:
            created = repo.create(entity_cls(**data))
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
        return read_schema.model_validate(created, from_attributes=True)

    @router.patch("/{item_id}", response_model=read_schema)
    def update_item(
        item_id: str,
        payload: update_schema,
        repo: InMemoryRepository = Depends(get_repo),
        _: object = Depends(get_current_admin),
    ):
        try:
            updated = repo.update(item_id, **payload.model_dump(exclude_unset=True))
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found") from exc
        return read_schema.model_validate(updated, from_attributes=True)

    @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(
        item_id: str,
        repo: InMemoryRepository = Depends(get_repo),
        _: object = Depends(get_current_admin),
    ):
        try:
            repo.delete(item_id)
        except KeyError as exc:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found") from exc

    return router
