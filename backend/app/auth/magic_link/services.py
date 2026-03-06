import logging
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.crypto import generate_secure_token, hash_token
from app.auth.models import MagicLinkToken
from app.emails.service import EmailService
from app.users.models import User
from app.utils.configure import Config

logger = logging.getLogger(__name__)

TOKEN_EXPIRY_MINUTES = 15


class MagicLinkService:
    """Handles magic link token creation and verification."""

    def __init__(self, db: AsyncSession, email_service: EmailService, config: Config) -> None:
        self.db = db
        self.email_service = email_service
        self.config = config

    async def create_and_send(self, email: str) -> None:
        """Create a magic link token for the email and send it. Always succeeds silently."""
        email = self.email_service.validate_email_address(email)

        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if user is None:
            name = email.split("@")[0]
            user = User(name=name, email=email, email_verified=False)
            self.db.add(user)
            await self.db.flush()

        token = generate_secure_token()
        token_hash = hash_token(token, self.config.SECRET_KEY)
        expires_at = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRY_MINUTES)

        self.db.add(MagicLinkToken(token_hash=token_hash, user_id=user.id, expires_at=expires_at))
        await self.db.commit()

        verify_url = f"{self.config.FRONTEND_ORIGIN.rstrip('/')}/auth/magic-link/verify?token={token}"
        await self.email_service.send_magic_link_email(
            to_email=email,
            magic_link_url=verify_url,
            expires_minutes=TOKEN_EXPIRY_MINUTES,
        )
        logger.info("Magic link sent to %s", email)

    async def verify(self, token: str) -> User | None:
        """Verify a magic link token. Returns the user on success, None if invalid/expired."""
        token_hash = hash_token(token, self.config.SECRET_KEY)
        now = datetime.now(UTC)

        result = await self.db.execute(
            select(MagicLinkToken).where(
                MagicLinkToken.token_hash == token_hash,
                MagicLinkToken.expires_at > now,
                MagicLinkToken.used_at.is_(None),
            )
        )
        ml_token = result.scalar_one_or_none()

        if ml_token is None:
            return None

        ml_token.used_at = now

        user_result = await self.db.execute(select(User).where(User.id == ml_token.user_id))
        user = user_result.scalar_one()
        user.email_verified = True
        await self.db.commit()

        return user
