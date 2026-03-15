from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.crypto import generate_secure_token, hash_token
from app.auth.models import OrgInvitationToken
from app.comms.service.emails import EmailService
from app.orgs.exceptions import DuplicateInvitationError, InvalidInvitationError
from app.orgs.queries import get_invitation_by_token_hash, get_pending_invitation
from app.users.models import User
from app.users.queries import create_user, get_user_by_email
from app.utils.configure import config

INVITE_EXPIRY_HOURS = 72


class OrgService:
    def __init__(
        self,
        transaction: AsyncSession,
        email_service: EmailService,
    ) -> None:
        self.db = transaction
        self.email_service = email_service

    async def accept_invitation(self, token: str, session: dict) -> None:
        """Validate and accept an org invitation token. Raises InvalidInvitationError if invalid."""
        token_hash = hash_token(token, config.SECRET_KEY)
        invite = await get_invitation_by_token_hash(self.db, token_hash)

        if not invite or not invite.is_valid():
            raise InvalidInvitationError

        user = await get_user_by_email(self.db, invite.invited_email)
        if user is None:
            name = invite.invited_email.split("@")[0]
            user = await create_user(
                self.db,
                name=name,
                email=invite.invited_email,
                organization_id=invite.organization_id,
            )

        user.email_verified = True
        invite.mark_accepted()
        await self.db.flush()

        session["user_id"] = user.id

    async def invite_user(self, email: str, invited_by: User) -> None:
        """Create and send an org invitation. Raises DuplicateInvitationError if already pending."""
        email = self.email_service.validate_email_address(email)

        existing = await get_pending_invitation(self.db, invited_by.organization_id, email.lower())
        if existing:
            raise DuplicateInvitationError

        token = generate_secure_token()
        token_hash = hash_token(token, config.SECRET_KEY)
        expires_at = datetime.now(UTC) + timedelta(hours=INVITE_EXPIRY_HOURS)

        invite = OrgInvitationToken(
            token_hash=token_hash,
            organization_id=invited_by.organization_id,
            invited_email=email.lower(),
            invited_by_user_id=invited_by.id,
            expires_at=expires_at,
        )
        self.db.add(invite)
        await self.db.flush()

        invite_url = f"{config.FRONTEND_ORIGIN.rstrip('/')}/invite/accept?token={token}"
        await self.email_service.send_org_invitation_email(
            to_email=email,
            inviter_name=invited_by.name,
            invitation_url=invite_url,
            expires_hours=INVITE_EXPIRY_HOURS,
        )
