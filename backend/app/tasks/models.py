from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.base.mixins import OrgScopedMixin, TimestampMixin
from app.base.models import BaseDBModel
from app.tasks.enums import TaskPriority, TaskStatus


class TaskSchedule(TimestampMixin, BaseDBModel):
    __tablename__ = "task_schedules"

    cron: Mapped[str] = mapped_column(sa.Text, nullable=False)


class Task(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "tasks"

    patient_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("patients.id", ondelete="SET NULL"), nullable=True, index=True
    )
    assigned_to_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    created_by_id: Mapped[int] = mapped_column(
        sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(sa.Text, nullable=False)
    description: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    priority: Mapped[TaskPriority] = mapped_column(
        sa.Text,
        nullable=False,
        default=TaskPriority.MEDIUM,
    )
    status: Mapped[TaskStatus] = mapped_column(
        sa.Text,
        nullable=False,
        default=TaskStatus.PENDING,
    )
    due_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(sa.DateTime(timezone=True), nullable=True)
