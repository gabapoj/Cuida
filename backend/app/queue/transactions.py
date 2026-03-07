"""Transaction helpers for SAQ tasks.

Provides:
  - task_transaction: async context manager wrapping a single DB transaction
  - @with_transaction: decorator that injects `transaction: AsyncSession` into a task
"""

from collections.abc import AsyncGenerator, Callable
from contextlib import asynccontextmanager
from functools import wraps
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@asynccontextmanager
async def task_transaction(
    db_sessionmaker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession]:
    """Async context manager that begins a transaction and commits or rolls back."""
    async with db_sessionmaker() as session:
        async with session.begin():
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


def with_transaction(fn: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that injects `transaction: AsyncSession` as a keyword argument.

    The wrapped task function must accept `ctx` as its first positional arg
    and `transaction` as a keyword argument.
    """

    @wraps(fn)
    async def wrapper(ctx: Any, **kwargs: Any) -> Any:
        async with task_transaction(ctx["db_sessionmaker"]) as session:
            return await fn(ctx, transaction=session, **kwargs)

    return wrapper
