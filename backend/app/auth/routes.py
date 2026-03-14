import logging
from dataclasses import dataclass

from litestar import Request, Router, get, post
from litestar.exceptions import PermissionDeniedException
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.response import Redirect

from app.auth.guards import requires_session
from app.auth.service import AuthService
from app.users.models import User
from app.utils.configure import config

logger = logging.getLogger(__name__)

_rate_limit = RateLimitConfig(rate_limit=("minute", 3))


@dataclass
class MagicLinkRequestBody:
    email: str


@post("/magic-link/request", tags=["auth"], middleware=[_rate_limit.middleware])
async def request_magic_link(
    data: MagicLinkRequestBody,
    auth_service: AuthService,
) -> dict[str, str]:
    """Request a magic link for the given email. Always returns success."""
    try:
        await auth_service.request_magic_link(data.email)
    except Exception:
        logger.exception("Failed to send magic link to %s", data.email)
    return {"message": "If that email exists, a magic link has been sent."}


@get("/magic-link/verify", tags=["auth"])
async def verify_magic_link(
    token: str,
    request: Request,
    auth_service: AuthService,
) -> Redirect:
    """Verify a magic link token, set session, and redirect to the frontend."""
    user = await auth_service.verify_magic_link(token)

    if user is None:
        raise PermissionDeniedException("Invalid or expired magic link.")

    request.set_session({"user_id": user.id})
    return Redirect(path=config.SUCCESS_REDIRECT_URL)


@post("/logout", tags=["auth"])
async def logout(request: Request) -> dict[str, str]:
    """Clear the current session."""
    request.clear_session()
    return {"message": "Logged out"}


@get("/me", guards=[requires_session], tags=["auth"])
async def me(user: User) -> dict:
    """Return the current authenticated user."""
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "email_verified": user.email_verified,
    }


auth_router = Router(
    path="/auth",
    route_handlers=[request_magic_link, verify_magic_link, logout, me],
    tags=["auth"],
)
