from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.base.mixins import OrgScopedMixin, TimestampMixin
from app.base.models import BaseDBModel
from app.llm.enums import MessageRole


class LLMThread(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "llm_threads"

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)


class LLMMessage(TimestampMixin, OrgScopedMixin, BaseDBModel):
    __tablename__ = "llm_messages"

    thread_id: Mapped[int] = mapped_column(
        sa.ForeignKey("llm_threads.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[MessageRole] = mapped_column(
        sa.Text,
        nullable=False,
    )
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    input_tokens: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(sa.Integer, nullable=True)
    model: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
