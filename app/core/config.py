from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables and `.env`."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Lamborghini Colección API"
    api_prefix: str = "/api/v1"
    debug: bool = True
    secret_key: str = "change-me-in-production-lamborghini-coleccion"
    access_token_expire_minutes: int = 60 * 12
    admin_email: str = "admin@example.com"
    admin_password: str = "Admin123!"
    database_url: str = "mysql+pymysql://root@127.0.0.1:3306/lb"
    persistence: str = "sql"
    cors_origins: list[str] = [
        "http://localhost:5180",
        "http://localhost:5181",
        "http://127.0.0.1:5180",
        "http://127.0.0.1:5181",
    ]


@lru_cache
def get_settings() -> Settings:
    """
    Return cached application settings.

    @return: Settings singleton instance
    """
    return Settings()
