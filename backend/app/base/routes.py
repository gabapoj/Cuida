from litestar import Router, get
from litestar.exceptions import ServiceUnavailableException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@get("/health", tags=["system"])
async def health_check(db_session: AsyncSession) -> dict[str, str]:
    """Health check endpoint.

    Runs a SELECT 1 against the database to verify connectivity.
    Returns 200 {"status": "ok", "db": "ok"} on success.
    Returns 503 {"detail": "Database unavailable"} on DB failure.

    Unauthenticated — used by load balancers, uptime monitors, and CI.
    """
    try:
        await db_session.execute(text("SELECT 1"))
    except Exception as exc:
        raise ServiceUnavailableException(detail="Database unavailable") from exc

    return {"status": "ok", "db": "ok"}


system_router = Router(
    path="/",
    route_handlers=[health_check],
    tags=["system"],
)
