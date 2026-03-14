from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import OrgInvitationToken


async def get_invitation_by_token_hash(db: AsyncSession, token_hash: str) -> OrgInvitationToken | None:
    result = await db.execute(
        select(OrgInvitationToken)
        .where(OrgInvitationToken.token_hash == token_hash)
        .where(OrgInvitationToken.accepted_at.is_(None))
        .with_for_update()
    )
    return result.scalar_one_or_none()


async def get_pending_invitation(db: AsyncSession, organization_id: int, email: str) -> OrgInvitationToken | None:
    result = await db.execute(
        select(OrgInvitationToken)
        .where(OrgInvitationToken.organization_id == organization_id)
        .where(OrgInvitationToken.invited_email == email)
        .where(OrgInvitationToken.accepted_at.is_(None))
    )
    return result.scalar_one_or_none()
