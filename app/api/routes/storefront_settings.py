from fastapi import APIRouter, Depends

from app.api.deps import get_setting_repo
from app.schemas.admin_resources import SettingRead

router = APIRouter(prefix="/storefront", tags=["storefront"])


@router.get("/settings", response_model=list[SettingRead])
def list_storefront_settings(repo=Depends(get_setting_repo)) -> list[SettingRead]:
    """
    Public active settings for the storefront (social links, store name, etc.).

    @return: Active setting DTOs
    """
    items = repo.list(active_only=True)
    return [SettingRead.model_validate(item, from_attributes=True) for item in items]
