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

    name: Mapped[str] = mapped_column(sa.Text, nullable=False)


class Address(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "addresses"

    line1: Mapped[str] = mapped_column(sa.Text, nullable=False)
    line2: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    city: Mapped[str] = mapped_column(sa.Text, nullable=False)
    state: Mapped[str] = mapped_column(sa.Text, nullable=False)
    postal_code: Mapped[str] = mapped_column(sa.Text, nullable=False)
    country: Mapped[str] = mapped_column(sa.Text, nullable=False, server_default="US")
    lat: Mapped[float | None] = mapped_column(sa.Float, nullable=True)
    lng: Mapped[float | None] = mapped_column(sa.Float, nullable=True)


class User(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "users"
    __table_args__ = (sa.Index("ix_users_email", "email", unique=True),)

    name: Mapped[str] = mapped_column(sa.Text, nullable=False)
    email: Mapped[str] = mapped_column(sa.Text, nullable=False)
    email_verified: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=False)
    phone: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    address_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("addresses.id", ondelete="SET NULL"), nullable=True, index=True
    )
    report_schedule_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("task_schedules.id", ondelete="SET NULL"), nullable=True, index=True
    )

    address: Mapped[Address | None] = relationship("Address", foreign_keys=[address_id])
    report_schedule: Mapped[TaskSchedule | None] = relationship("TaskSchedule", foreign_keys=[report_schedule_id])


class Patient(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "patients"

    primary_caregiver_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    address_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("addresses.id", ondelete="SET NULL"), nullable=True, index=True
    )
    call_schedule_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("task_schedules.id", ondelete="SET NULL"), nullable=True, index=True
    )
    name: Mapped[str] = mapped_column(sa.Text, nullable=False)
    dob: Mapped[date | None] = mapped_column(sa.Date, nullable=True)
    phone: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    email: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(sa.Text, nullable=True)

    primary_caregiver: Mapped[User | None] = relationship("User", foreign_keys=[primary_caregiver_id])
    address: Mapped[Address | None] = relationship("Address", foreign_keys=[address_id])
    call_schedule: Mapped[TaskSchedule | None] = relationship("TaskSchedule", foreign_keys=[call_schedule_id])
