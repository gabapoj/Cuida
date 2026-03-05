from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseDBModel(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    Provides standard audit columns on every table:
    - id:         integer primary key (autoincrement)
    - created_at: set on INSERT via server default
    - updated_at: set on INSERT and UPDATE via server default / onupdate
    - deleted_at: nullable — set by soft_delete(), cleared by restore()

    Usage:
        class User(BaseDBModel):
            __tablename__ = "users"
            email: Mapped[str] = mapped_column(unique=True)
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        index=True,
    )

    def to_dict(self) -> dict[str, Any]:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

    def soft_delete(self) -> None:
        self.deleted_at = datetime.now(tz=UTC)

    def restore(self) -> None:
        self.deleted_at = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
