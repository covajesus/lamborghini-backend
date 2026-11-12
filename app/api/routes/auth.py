from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service, get_current_admin
from app.domain.entities import AdminUser
from app.schemas.auth import AdminProfile, LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    try:
        user = service.authenticate(payload.email, payload.password)
    except PermissionError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials") from exc
    return TokenResponse(access_token=service.issue_token(user))


@router.get("/me", response_model=AdminProfile)
def me(user: AdminUser = Depends(get_current_admin)) -> AdminProfile:
    return AdminProfile(id=user.id, email=user.email, full_name=user.full_name, role=user.role)
