from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Hash a plain password for secure storage.

    @param password: Plain text password input
    @return: Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a stored hash.

    @param plain_password: Plain text password input
    @param hashed_password: Stored password hash
    @return: True when the password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, claims: dict[str, Any] | None = None) -> str:
    """
    Issue a signed JWT access token.

    @param subject: Token subject (admin user id)
    @param claims: Optional extra JWT claims
    @return: Encoded JWT string
    """
    settings = get_settings()
    payload: dict[str, Any] = {
        "sub": subject,
        "exp": datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes),
    }
    if claims:
        payload.update(claims)
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.

    @param token: Encoded JWT string
    @return: Decoded token payload
    """
    settings = get_settings()
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
