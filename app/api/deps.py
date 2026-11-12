from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_access_token
from app.domain.entities import AdminUser
from app.services.auth_service import AuthService
from app.services.product_service import ProductService

bearer = HTTPBearer(auto_error=False)

_product_repo: Any = None
_user_repo: Any = None
_inventory_repo: Any = None
_payment_repo: Any = None
_staff_repo: Any = None
_setting_repo: Any = None
_slides_repo: Any = None
_categories_repo: Any = None
_roles_repo: Any = None


def configure_repositories(
    products: Any,
    users: Any,
    inventory: Any = None,
    payments: Any = None,
    staff_users: Any = None,
    settings: Any = None,
    slides: Any = None,
    categories: Any = None,
    roles: Any = None,
) -> None:
    """
    Register repository implementations for dependency injection.

    @param products: Product repository instance
    @param users: Auth user repository instance
    @param inventory: Inventory repository instance
    @param payments: Payments repository instance
    @param staff_users: Staff users repository instance
    @param settings: Settings repository instance
    @param slides: Slides repository instance
    @param categories: Categories repository instance
    @param roles: Roles repository instance
    @return: None
    """
    global _product_repo, _user_repo, _inventory_repo, _payment_repo, _staff_repo, _setting_repo, _slides_repo, _categories_repo, _roles_repo
    _product_repo = products
    _user_repo = users
    _inventory_repo = inventory
    _payment_repo = payments
    _staff_repo = staff_users
    _setting_repo = settings
    _slides_repo = slides
    _categories_repo = categories
    _roles_repo = roles


def get_product_service() -> ProductService:
    """
    Provide a ProductService bound to the configured product repository.

    @return: ProductService instance
    """
    if _product_repo is None:
        raise RuntimeError("Product repository is not configured")
    return ProductService(_product_repo)


def get_auth_service() -> AuthService:
    """
    Provide an AuthService bound to the configured user repository.

    @return: AuthService instance
    """
    if _user_repo is None:
        raise RuntimeError("User repository is not configured")
    return AuthService(_user_repo)


def get_inventory_repo() -> Any:
    """
    @return: Inventory repository
    """
    if _inventory_repo is None:
        raise RuntimeError("Inventory repository is not configured")
    return _inventory_repo


def get_payment_repo() -> Any:
    """
    @return: Payment repository
    """
    if _payment_repo is None:
        raise RuntimeError("Payment repository is not configured")
    return _payment_repo


def get_staff_repo() -> Any:
    """
    @return: Staff users repository
    """
    if _staff_repo is None:
        raise RuntimeError("Staff repository is not configured")
    return _staff_repo


def get_setting_repo() -> Any:
    """
    @return: Settings repository
    """
    if _setting_repo is None:
        raise RuntimeError("Settings repository is not configured")
    return _setting_repo


def get_slides_repo() -> Any:
    """
    @return: Slides repository
    """
    if _slides_repo is None:
        raise RuntimeError("Slides repository is not configured")
    return _slides_repo


def get_categories_repo() -> Any:
    """
    @return: Categories repository
    """
    if _categories_repo is None:
        raise RuntimeError("Categories repository is not configured")
    return _categories_repo


def get_roles_repo() -> Any:
    """
    @return: Roles repository
    """
    if _roles_repo is None:
        raise RuntimeError("Roles repository is not configured")
    return _roles_repo


def get_current_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> AdminUser:
    """
    Resolve the authenticated admin from the Bearer JWT.

    @param credentials: HTTP Authorization header credentials
    @return: Authenticated AdminUser entity
    """
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    if _user_repo is None:
        raise RuntimeError("User repository is not configured")
    user = _user_repo.get_by_id(str(payload.get("sub")))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
