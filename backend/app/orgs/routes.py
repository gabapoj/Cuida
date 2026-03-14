from litestar import Request, Router, get
from litestar.response import Redirect

from app.orgs.exceptions import InvalidInvitationError
from app.orgs.service import OrgService
from app.utils.configure import config


@get("/invite/accept")
async def accept_org_invitation(
    token: str,
    request: Request,
    org_service: OrgService,
) -> Redirect:
    frontend = config.FRONTEND_ORIGIN.rstrip("/")
    try:
        await org_service.accept_invitation(token, request.session)
    except InvalidInvitationError:
        return Redirect(path=f"{frontend}/auth?error=invalid_invitation")
    return Redirect(path=f"{frontend}/")


invite_router = Router(path="", route_handlers=[accept_org_invitation])
