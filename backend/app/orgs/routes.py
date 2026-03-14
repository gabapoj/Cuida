from litestar import Request, Router, get
from litestar.response import Redirect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.crypto import hash_token
from app.auth.models import OrgInvitationToken
from app.users.queries import create_user, get_user_by_email
from app.utils.configure import Config


@get("/invite/accept")
async def accept_org_invitation(
    token: str,
    transaction: AsyncSession,
    request: Request,
    config: Config,
) -> Redirect:
    token_hash = hash_token(token, config.SECRET_KEY)

    result = await transaction.execute(
        select(OrgInvitationToken)
        .where(OrgInvitationToken.token_hash == token_hash)
        .where(OrgInvitationToken.accepted_at.is_(None))
        .with_for_update()
    )
    invite = result.scalar_one_or_none()

    frontend = config.FRONTEND_ORIGIN.rstrip("/")
    if not invite or not invite.is_valid():
        return Redirect(path=f"{frontend}/auth?error=invalid_invitation")

    user = await get_user_by_email(transaction, invite.invited_email)
    if user is None:
        name = invite.invited_email.split("@")[0]
        user = await create_user(
            transaction,
            name=name,
            email=invite.invited_email,
            organization_id=invite.organization_id,
        )
    user.email_verified = True
    invite.mark_accepted()
    await transaction.flush()

    request.session["user_id"] = user.id
    return Redirect(path=f"{frontend}/")


invite_router = Router(path="", route_handlers=[accept_org_invitation])
