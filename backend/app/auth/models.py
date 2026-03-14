from datetime import UTC, datetime

import sqlalchemy as sa
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.base.mixins import TimestampMixin
from app.base.models import BaseDBModel


class MagicLinkToken(TimestampMixin, BaseDBModel):
    __tablename__ = "magic_link_tokens"

    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class OrgInvitationToken(TimestampMixin, BaseDBModel):
    __tablename__ = "org_invitation_tokens"
    __table_args__ = (
        sa.Index(
            "ix_org_invitation_pending",
            "organization_id",
            "invited_email",
            unique=True,
            postgresql_where=sa.text("accepted_at IS NULL"),
        ),
    )

    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)
    invited_email: Mapped[str] = mapped_column(sa.Text, index=True)
    invited_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    def is_valid(self) -> bool:
        return self.accepted_at is None and self.expires_at > datetime.now(UTC)

    def mark_accepted(self) -> None:
        self.accepted_at = datetime.now(UTC)
