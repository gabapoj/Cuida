"""Email service."""

import logging
from typing import Any

from email_validator import EmailNotValidError, validate_email
from litestar import Request
from litestar.contrib.jinja import JinjaTemplateEngine
from sqlalchemy.ext.asyncio import AsyncSession

from app.comms.enums import EmailMessageStatus
from app.comms.models.emails import EmailMessage as EmailMessageRecord
from app.queue.registry import TaskName
from app.queue.transactions import dispatch_task
from app.utils.configure import config

logger = logging.getLogger(__name__)


class EmailService:
    """High-level email service with template rendering and send-attempt tracking."""

    def __init__(self, template_engine: JinjaTemplateEngine, transaction: AsyncSession, request: Request):
        self.template_engine = template_engine
        self.transaction = transaction
        self.request = request

    def validate_email_address(self, email: str) -> str:
        """Validate and normalize an email address."""
        try:
            valid = validate_email(email, check_deliverability=False)
            return valid.normalized
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {email}") from e

    def render_template(self, template_name: str, context: dict[str, Any]) -> tuple[str, str]:
        """Render email template, returning (html, text) tuple."""
        jinja_env = self.template_engine.engine

        html_body = jinja_env.get_template(f"{template_name}/html.jinja2").render(**context)
        text_body = jinja_env.get_template(f"{template_name}/text.jinja2").render(**context)

        return html_body, text_body

    async def send_email(
        self,
        to: list[str] | str,
        subject: str,
        template_name: str,
        context: dict[str, Any],
        from_email: str | None = None,
        from_name: str | None = None,
        reply_to: str | None = None,
    ) -> int:
        if isinstance(to, str):
            to = [to]

        to = [self.validate_email_address(email) for email in to]

        from_email = from_email or config.SES_FROM_EMAIL
        from_name = from_name or config.SES_FROM_NAME
        reply_to = reply_to or config.SES_REPLY_TO_EMAIL

        html_body, text_body = self.render_template(template_name, context)

        record = EmailMessageRecord(
            to_email=to,
            from_email=from_email,
            from_name=from_name,
            reply_to_email=reply_to,
            subject=subject,
            body_html=html_body,
            body_text=text_body,
            template_name=template_name,
            status=EmailMessageStatus.PENDING,
        )
        self.transaction.add(record)
        await self.transaction.flush()

        await dispatch_task(self.transaction, self.request, TaskName.SEND_EMAIL, email_message_id=record.id)

        return record.id

    async def send_magic_link_email(
        self,
        to_email: str,
        magic_link_url: str,
        expires_minutes: int = 15,
    ) -> None:
        """Send magic link login email."""
        await self.send_email(
            to=to_email,
            subject="Sign in to Nearwise",
            template_name="magic_link",
            context={
                "magic_link_url": magic_link_url,
                "expiration_minutes": expires_minutes,
            },
        )

    async def send_signup_confirmation_email(
        self,
        to_email: str,
    ) -> None:
        """Send welcome email after signup."""
        await self.send_email(
            to=to_email,
            subject="Welcome to Nearwise",
            template_name="signup_confirmation",
            context={"user_email": to_email},
        )

    async def send_org_invitation_email(
        self,
        to_email: str,
        inviter_name: str,
        invitation_url: str,
        expires_hours: int = 72,
    ) -> None:
        """Send organisation invitation email."""
        await self.send_email(
            to=to_email,
            subject=f"{inviter_name} invited you to join",
            template_name="org_invitation",
            context={
                "inviter_name": inviter_name,
                "invitation_url": invitation_url,
                "expiration_hours": expires_hours,
            },
        )
