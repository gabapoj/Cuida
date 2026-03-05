import logging
from dataclasses import dataclass

from litestar import Request, Router, get, post
from litestar.exceptions import PermissionDeniedException
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.response import Redirect
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.magic_link.services import MagicLinkService
from app.emails.service import EmailService
from app.utils.configure import Config

logger = logging.getLogger(__name__)

_rate_limit = RateLimitConfig(rate_limit=("minute", 3))


@dataclass
class MagicLinkRequestBody:
    email: str


@post("/request", tags=["auth"], middleware=[_rate_limit.middleware])
async def request_magic_link(
    data: MagicLinkRequestBody,
    db_session: AsyncSession,
    email_service: EmailService,
    config: Config,
) -> dict[str, str]:
    """Request a magic link for the given email. Always returns success."""
    service = MagicLinkService(db_session, email_service, config)
    try:
        await service.create_and_send(data.email)
    except Exception:
        logger.exception("Failed to send magic link to %s", data.email)
    return {"message": "If that email exists, a magic link has been sent."}


@get("/verify", tags=["auth"])
async def verify_magic_link(
    token: str,
    request: Request,
    db_session: AsyncSession,
    email_service: EmailService,
    config: Config,
) -> Redirect:
    """Verify a magic link token, set session, and redirect to the frontend."""
    service = MagicLinkService(db_session, email_service, config)
    user = await service.verify(token)

    if user is None:
        raise PermissionDeniedException("Invalid or expired magic link.")

    request.set_session({"user_id": user.id})
    return Redirect(path=config.SUCCESS_REDIRECT_URL)


magic_link_router = Router(
    path="/magic-link",
    route_handlers=[request_magic_link, verify_magic_link],
)
