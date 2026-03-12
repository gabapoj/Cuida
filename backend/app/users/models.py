from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.base.mixins import OrgScopedMixin, TimestampMixin
from app.base.models import BaseDBModel

if TYPE_CHECKING:
    from app.tasks.models import TaskSchedule


class Organization(TimestampMixin, BaseDBModel):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(sa.Text)


class Address(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "addresses"

    line1: Mapped[str] = mapped_column(sa.Text)
    line2: Mapped[str | None] = mapped_column(sa.Text)
    city: Mapped[str] = mapped_column(sa.Text)
    state: Mapped[str] = mapped_column(sa.Text)
    postal_code: Mapped[str] = mapped_column(sa.Text)
    country: Mapped[str] = mapped_column(sa.Text, server_default="US")
    lat: Mapped[float | None] = mapped_column()
    lng: Mapped[float | None] = mapped_column()


class User(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "users"
    __table_args__ = (sa.Index("ix_users_email", "email", unique=True),)

    name: Mapped[str] = mapped_column(sa.Text)
    email: Mapped[str] = mapped_column(sa.Text)
    email_verified: Mapped[bool] = mapped_column(default=False)
    phone: Mapped[str | None] = mapped_column(sa.Text)
    address_id: Mapped[int | None] = mapped_column(sa.ForeignKey("addresses.id", ondelete="SET NULL"), index=True)
    report_schedule_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("task_schedules.id", ondelete="SET NULL"), index=True
    )

    address: Mapped[Address | None] = relationship("Address", foreign_keys=[address_id])
    report_schedule: Mapped[TaskSchedule | None] = relationship("TaskSchedule", foreign_keys=[report_schedule_id])


class Patient(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "patients"

    address_id: Mapped[int | None] = mapped_column(sa.ForeignKey("addresses.id", ondelete="SET NULL"), index=True)
    call_schedule_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("task_schedules.id", ondelete="SET NULL"), index=True
    )
    name: Mapped[str] = mapped_column(sa.Text)
    dob: Mapped[date | None] = mapped_column()
    notes: Mapped[str | None] = mapped_column(sa.Text)

    address: Mapped[Address | None] = relationship("Address", foreign_keys=[address_id])
    call_schedule: Mapped[TaskSchedule | None] = relationship("TaskSchedule", foreign_keys=[call_schedule_id])
