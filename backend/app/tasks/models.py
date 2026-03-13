from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.base.mixins import OrgScopedMixin, TimestampMixin
from app.base.models import BaseDBModel
from app.tasks.enums import TaskStatus


class TaskSchedule(TimestampMixin, BaseDBModel):
    __tablename__ = "task_schedules"

    cron: Mapped[str] = mapped_column(sa.Text)


class Task(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "tasks"

    queue: Mapped[str] = mapped_column(sa.Text)
    job_key: Mapped[str] = mapped_column(sa.Text, index=True)
    status: Mapped[TaskStatus] = mapped_column(sa.Text)
    error: Mapped[str | None] = mapped_column(sa.Text)
