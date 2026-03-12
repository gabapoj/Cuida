"""Email message models."""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.base.mixins import TimestampMixin
from app.base.models import BaseDBModel


class EmailMessage(TimestampMixin, BaseDBModel):
    """Outbound email messages — one row per send attempt."""

    __tablename__ = "email_messages"

    # Recipients
    to_email: Mapped[str] = mapped_column(sa.Text, nullable=False)
    from_email: Mapped[str] = mapped_column(sa.Text, nullable=False)
    reply_to_email: Mapped[str | None] = mapped_column(sa.Text)

    # Content
    subject: Mapped[str] = mapped_column(sa.Text, nullable=False)
    body_html: Mapped[str] = mapped_column(sa.Text, nullable=False)
    body_text: Mapped[str] = mapped_column(sa.Text, nullable=False)

    # SES tracking
    ses_message_id: Mapped[str | None] = mapped_column(sa.Text, unique=True)
    sent_at: Mapped[datetime | None]

    # Metadata
    template_name: Mapped[str | None] = mapped_column(sa.Text)

    def __repr__(self) -> str:
        return f"<EmailMessage(id={self.id}, to={self.to_email}, subject={self.subject[:30]})>"
