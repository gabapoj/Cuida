from litestar import Router, get
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@get("/health", tags=["system"])
async def health_check(db_session: AsyncSession) -> dict[str, str]:
    await db_session.execute(text("SELECT 1"))
    return {"status": "ok", "db": "ok"}


system_router = Router(
    path="/",
    route_handlers=[health_check],
    tags=["system"],
)
