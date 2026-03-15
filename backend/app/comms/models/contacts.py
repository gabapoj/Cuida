from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.base.mixins import OrgScopedMixin, TimestampMixin
from app.base.models import BaseDBModel
from app.comms.enums import ContactType, Direction, PhoneCallStatus, TextMessageStatus


class Contact(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "contacts"

    patient_id: Mapped[int | None] = mapped_column(sa.ForeignKey("patients.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int | None] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), index=True)
    type: Mapped[ContactType] = mapped_column(sa.Text)
    value: Mapped[str] = mapped_column(sa.Text)


class TextMessage(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "text_messages"

    contact_id: Mapped[int] = mapped_column(sa.ForeignKey("contacts.id", ondelete="RESTRICT"), index=True)
    direction: Mapped[Direction] = mapped_column(sa.Text)
    body: Mapped[str] = mapped_column(sa.Text)
    status: Mapped[TextMessageStatus] = mapped_column(sa.Text)
    provider_message_id: Mapped[str | None] = mapped_column(sa.Text)


class PhoneCall(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "phone_calls"

    contact_id: Mapped[int] = mapped_column(sa.ForeignKey("contacts.id", ondelete="RESTRICT"), index=True)
    direction: Mapped[Direction] = mapped_column(sa.Text)
    status: Mapped[PhoneCallStatus] = mapped_column(sa.Text)
    duration_seconds: Mapped[int | None] = mapped_column()
    recording_url: Mapped[str | None] = mapped_column(sa.Text)
    transcript: Mapped[str | None] = mapped_column(sa.Text)
    provider_call_id: Mapped[str | None] = mapped_column(sa.Text)
