from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.base.mixins import OrgScopedMixin, TimestampMixin
from app.base.models import BaseDBModel
from app.calendar.enums import CalendarEventType


class CalendarEvent(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "calendar_events"

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="RESTRICT"), index=True)
    patient_id: Mapped[int | None] = mapped_column(sa.ForeignKey("patients.id", ondelete="SET NULL"), index=True)
    event_type: Mapped[CalendarEventType] = mapped_column(
        sa.Text,
    )
    title: Mapped[str] = mapped_column(sa.Text)
    description: Mapped[str | None] = mapped_column(sa.Text)
    start_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    end_at: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True))
    cancelled_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True))
