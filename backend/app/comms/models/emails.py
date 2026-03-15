"""Email message models."""

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.base.mixins import TimestampMixin
from app.base.models import BaseDBModel
from app.comms.enums import EmailMessageStatus


class EmailMessage(TimestampMixin, BaseDBModel):
    """Outbound email messages — one row per send attempt."""

    __tablename__ = "email_messages"

    # Recipients
    to_email: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.Text))
    from_email: Mapped[str] = mapped_column(sa.Text)
    from_name: Mapped[str | None] = mapped_column(sa.Text)
    reply_to_email: Mapped[str | None] = mapped_column(sa.Text)

    # Content
    subject: Mapped[str] = mapped_column(sa.Text)
    body_html: Mapped[str] = mapped_column(sa.Text)
    body_text: Mapped[str] = mapped_column(sa.Text)

    # SES tracking
    ses_message_id: Mapped[str | None] = mapped_column(sa.Text, unique=True)
    sent_at: Mapped[datetime | None]

    # Attempt outcome
    status: Mapped[EmailMessageStatus] = mapped_column(
        sa.Enum(EmailMessageStatus, name="emailmessagestatus"),
        default=EmailMessageStatus.PENDING,
    )
    error_message: Mapped[str | None] = mapped_column(sa.Text)

    # Metadata
    template_name: Mapped[str | None] = mapped_column(sa.Text)

    def __repr__(self) -> str:
        return f"<EmailMessage(id={self.id}, to={self.to_email[0] if self.to_email else ''}, status={self.status})>"
