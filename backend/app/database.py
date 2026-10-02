"""SQLAlchemy async database setup — SQLite locally, swappable to PostgreSQL."""
from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()


def _resolve_db_url() -> str:
    """
    Resolve the database URL.
    - On Render with a persistent disk, DATABASE_URL points to /opt/render/project/data/
    - Locally it defaults to ./scamshield.db
    - Ensures the parent directory exists before SQLite tries to create the file.
    """
    url = settings.database_url
    if url.startswith("sqlite"):
        # Extract the file path from sqlite+aiosqlite:///path or sqlite:///path
        raw = url.split("///", 1)[-1]
        if raw and raw != ":memory:":
            db_path = Path(raw)
            db_path.parent.mkdir(parents=True, exist_ok=True)
    return url


_db_url = _resolve_db_url()

engine = create_async_engine(
    _db_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False} if "sqlite" in _db_url else {},
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    """Create all tables on startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:  # type: ignore[return]
    """FastAPI dependency — yields an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
