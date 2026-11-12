from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.db.mappers import admin_to_entity, admin_to_model
from app.db.models import AdminUserModel
from app.domain.entities import AdminUser


class SqlUserRepository:
    """MySQL-backed admin user repository."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        """
        @param session_factory: SQLAlchemy session factory
        @return: None
        """
        self._session_factory = session_factory

    def get_by_email(self, email: str) -> AdminUser | None:
        """
        @param email: Admin email
        @return: AdminUser or None
        """
        with self._session_factory() as session:
            row = session.scalar(select(AdminUserModel).where(AdminUserModel.email == email.lower()))
            if row is None:
                row = session.scalar(select(AdminUserModel).where(AdminUserModel.email == email))
            return admin_to_entity(row) if row else None

    def get_by_id(self, user_id: str) -> AdminUser | None:
        """
        @param user_id: Admin identifier
        @return: AdminUser or None
        """
        with self._session_factory() as session:
            row = session.get(AdminUserModel, user_id)
            return admin_to_entity(row) if row else None

    def create(self, user: AdminUser) -> AdminUser:
        """
        @param user: AdminUser entity
        @return: Stored AdminUser
        """
        with self._session_factory() as session:
            row = admin_to_model(user)
            session.add(row)
            session.commit()
            session.refresh(row)
            return admin_to_entity(row)
