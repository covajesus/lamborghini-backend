from app.core.security import create_access_token, verify_password
from app.domain.entities import AdminUser
class AuthService:
    """Authentication use-cases for admin users."""

    def __init__(self, users) -> None:
        """
        Create an auth service.

        @param users: User repository implementation
        @return: None
        """
        self._users = users

    def authenticate(self, email: str, password: str) -> AdminUser:
        """
        Validate admin credentials.

        @param email: Admin email input
        @param password: Plain password input
        @return: Authenticated AdminUser entity
        """
        user = self._users.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise PermissionError("Invalid credentials")
        return user

    def issue_token(self, user: AdminUser) -> str:
        """
        Issue a JWT for an authenticated admin.

        @param user: Authenticated AdminUser entity
        @return: Encoded JWT access token
        """
        return create_access_token(user.id, {"email": user.email, "role": user.role})
