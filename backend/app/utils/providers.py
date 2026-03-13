from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


async def provide_transaction(db_session: AsyncSession) -> AsyncGenerator[AsyncSession]:
    """Wrap the session in a transaction. Auto-commits on success, rolls back on exception."""
    async with db_session.begin():
        yield db_session
