from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.base.mixins import OrgScopedMixin, TimestampMixin
from app.base.models import BaseDBModel


class LLMThread(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "llm_threads"

    patient_id: Mapped[int | None] = mapped_column(sa.ForeignKey("patients.id", ondelete="SET NULL"), index=True)
    user_id: Mapped[int | None] = mapped_column(sa.ForeignKey("users.id", ondelete="SET NULL"), index=True)
    phone_call_id: Mapped[int | None] = mapped_column(sa.ForeignKey("phone_calls.id", ondelete="SET NULL"), index=True)
    text_message_id: Mapped[int | None] = mapped_column(
        sa.ForeignKey("text_messages.id", ondelete="SET NULL"), index=True
    )


class LLMMessage(TimestampMixin, BaseDBModel):
    __tablename__ = "llm_messages"

    thread_id: Mapped[int] = mapped_column(sa.ForeignKey("llm_threads.id", ondelete="CASCADE"), index=True)
    role: Mapped[str] = mapped_column(sa.Text)
    content: Mapped[str] = mapped_column(sa.Text)
