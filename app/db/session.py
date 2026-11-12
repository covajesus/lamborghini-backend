from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

_engine = None
_SessionLocal: sessionmaker[Session] | None = None


def get_engine():
    """
    Create or return the shared SQLAlchemy engine.

    @return: SQLAlchemy Engine
    """
    global _engine, _SessionLocal
    if _engine is None:
        settings = get_settings()
        connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
        _engine = create_engine(settings.database_url, pool_pre_ping=True, connect_args=connect_args)
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, expire_on_commit=False)
    return _engine


def get_session_factory() -> sessionmaker[Session]:
    """
    @return: Configured sessionmaker
    """
    get_engine()
    assert _SessionLocal is not None
    return _SessionLocal


def session_scope() -> Iterator[Session]:
    """
    Yield a short-lived database session.

    @return: SQLAlchemy Session iterator
    """
    factory = get_session_factory()
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def reset_engine() -> None:
    """
    Drop cached engine/session (useful in tests).

    @return: None
    """
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None
