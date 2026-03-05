from litestar import Request, Router, get, post
from litestar.exceptions import NotAuthorizedException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.guards import requires_session
from app.auth.magic_link.routes import magic_link_router
from app.users.models import User


@post("/logout", tags=["auth"])
async def logout(request: Request) -> dict[str, str]:
    """Clear the current session."""
    request.clear_session()
    return {"message": "Logged out"}


@get("/me", guards=[requires_session], tags=["auth"])
async def me(request: Request, db_session: AsyncSession) -> dict:
    """Return the current authenticated user."""
    user_id = request.session.get("user_id")
    result = await db_session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise NotAuthorizedException("User not found")
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "email_verified": user.email_verified,
    }


auth_router = Router(
    path="/auth",
    route_handlers=[magic_link_router, logout, me],
    tags=["auth"],
)
