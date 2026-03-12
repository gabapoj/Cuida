from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.base.mixins import OrgScopedMixin, TimestampMixin
from app.base.models import BaseDBModel
from app.comms.enums import Direction, PhoneCallStatus, TextMessageStatus


class PhoneNumber(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "phone_numbers"

    number: Mapped[str] = mapped_column(sa.Text, nullable=False)


class TextMessage(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "text_messages"

    phone_number_id: Mapped[int] = mapped_column(
        sa.ForeignKey("phone_numbers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    user_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    patient_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("patients.id", ondelete="SET NULL"), nullable=True, index=True
    )
    direction: Mapped[Direction] = mapped_column(
        sa.Enum(Direction, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    body: Mapped[str] = mapped_column(sa.Text, nullable=False)
    status: Mapped[TextMessageStatus] = mapped_column(
        sa.Enum(TextMessageStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    provider_message_id: Mapped[str | None] = mapped_column(sa.Text, nullable=True)


class PhoneCall(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "phone_calls"

    phone_number_id: Mapped[int] = mapped_column(
        sa.ForeignKey("phone_numbers.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    user_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    patient_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("patients.id", ondelete="SET NULL"), nullable=True, index=True
    )
    direction: Mapped[Direction] = mapped_column(
        sa.Enum(Direction, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    status: Mapped[PhoneCallStatus] = mapped_column(
        sa.Enum(PhoneCallStatus, native_enum=False, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
    )
    duration_seconds: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    recording_url: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    transcript: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    provider_call_id: Mapped[str | None] = mapped_column(sa.Text, nullable=True)


class Notification(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "notifications"

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(sa.Text, nullable=False)
    title: Mapped[str] = mapped_column(sa.Text, nullable=False)
    body: Mapped[str] = mapped_column(sa.Text, nullable=False)
    action_url: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    read_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True), nullable=True)
