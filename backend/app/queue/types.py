"""Typed AppContext for SAQ tasks.

Extend this when Phase 3 clients (OpenAI, S3, etc.) are added.
"""

from typing import Required

from saq.types import Context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.utils.configure import Config


class AppContext(Context):
    db_sessionmaker: Required[async_sessionmaker[AsyncSession]]
    config: Required[Config]
