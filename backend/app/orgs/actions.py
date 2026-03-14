from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.actions.base import BaseTopLevelAction, action_group_factory
from app.actions.deps import ActionDeps
from app.actions.enums import ActionGroupType, ActionIcon
from app.actions.schemas import ActionExecutionResponse
from app.auth.crypto import generate_secure_token, hash_token
from app.auth.models import OrgInvitationToken
from app.orgs.enums import OrgActions
from app.orgs.schemas import InviteUserSchema

INVITE_EXPIRY_HOURS = 72

org_actions = action_group_factory(ActionGroupType.ORG_ACTIONS)


@org_actions
class InviteUser(BaseTopLevelAction[InviteUserSchema]):
    action_key = OrgActions.INVITE_USER
    label = "Invite User"
    icon = ActionIcon.ADD
    priority = 10

    @classmethod
    def is_available(cls, obj, deps: ActionDeps) -> bool:
        return deps.user is not None

    @classmethod
    async def execute(
        cls, data: InviteUserSchema, transaction: AsyncSession, deps: ActionDeps
    ) -> ActionExecutionResponse:
        email = deps.email_service.validate_email_address(data.email)
        org_id = deps.user.organization_id

        # Check for existing pending invite
        existing = await transaction.execute(
            select(OrgInvitationToken)
            .where(OrgInvitationToken.organization_id == org_id)
            .where(OrgInvitationToken.invited_email == email.lower())
            .where(OrgInvitationToken.accepted_at.is_(None))
        )
        if existing.scalar_one_or_none():
            return ActionExecutionResponse(message="Invitation already sent")

        token = generate_secure_token()
        token_hash = hash_token(token, deps.config.SECRET_KEY)
        expires_at = datetime.now(UTC) + timedelta(hours=INVITE_EXPIRY_HOURS)

        invite = OrgInvitationToken(
            token_hash=token_hash,
            organization_id=org_id,
            invited_email=email.lower(),
            invited_by_user_id=deps.user.id,
            expires_at=expires_at,
        )
        transaction.add(invite)
        await transaction.flush()

        invite_url = f"{deps.config.FRONTEND_ORIGIN.rstrip('/')}/invite/accept?token={token}"
        await deps.email_service.send_org_invitation_email(
            to_email=email,
            inviter_name=deps.user.name,
            invitation_url=invite_url,
            expires_hours=INVITE_EXPIRY_HOURS,
        )
        return ActionExecutionResponse(message="Invitation sent")
