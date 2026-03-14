"""Email client and service."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Annotated, Any

import aioboto3
from email_validator import EmailNotValidError, validate_email
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.params import Dependency

from app.utils.configure import ConfigProtocol, config

logger = logging.getLogger(__name__)


@dataclass
class EmailMessage:
    """Email message data."""

    to: list[str]
    subject: str
    body_html: str
    body_text: str
    from_email: str
    from_name: str | None = None
    reply_to: str | None = None


class BaseEmailClient(ABC):
    """Abstract base class for email clients."""

    @abstractmethod
    async def send_email(self, message: EmailMessage) -> str:
        """Send an email. Returns message ID."""
        pass


class LocalEmailClient(BaseEmailClient):
    """Local email client that logs to console (for development)."""

    async def send_email(self, message: EmailMessage) -> str:
        """Log email instead of sending."""
        from_header = f'"{message.from_name}" <{message.from_email}>' if message.from_name else message.from_email

        logger.info("=" * 80)
        logger.info("LOCAL EMAIL (not actually sent)")
        logger.info(f"To: {', '.join(message.to)}")
        logger.info(f"From: {from_header}")
        logger.info(f"Subject: {message.subject}")
        logger.info(f"Reply-To: {message.reply_to}")
        logger.info("-" * 80)
        logger.info(f"HTML Body:\n{message.body_html}")
        logger.info("-" * 80)
        logger.info(f"Text Body:\n{message.body_text}")
        logger.info("=" * 80)

        return f"local-{hash(message.subject)}"


class SESEmailClient(BaseEmailClient):
    """AWS SES email client (async)."""

    def __init__(self, config: ConfigProtocol):
        self.region = config.SES_REGION
        self.configuration_set = config.SES_CONFIGURATION_SET

    async def send_email(self, message: EmailMessage) -> str:
        """Send email via AWS SES."""
        session = aioboto3.Session()

        async with session.client("ses", region_name=self.region) as ses:  # type: ignore[attr-defined]
            from_header = f'"{message.from_name}" <{message.from_email}>' if message.from_name else message.from_email

            msg = MIMEMultipart("alternative")
            msg["Subject"] = message.subject
            msg["From"] = from_header
            msg["To"] = ", ".join(message.to)

            if message.reply_to:
                msg["Reply-To"] = message.reply_to

            msg.attach(MIMEText(message.body_text, "plain", "utf-8"))
            msg.attach(MIMEText(message.body_html, "html", "utf-8"))

            kwargs: dict = {
                "Source": message.from_email,
                "Destinations": message.to,
                "RawMessage": {"Data": msg.as_string()},
            }

            if self.configuration_set:
                kwargs["ConfigurationSetName"] = self.configuration_set

            response = await ses.send_raw_email(**kwargs)

            logger.info(f"Email sent via SES: {response['MessageId']}")
            return response["MessageId"]


EmailClientDep = Annotated[BaseEmailClient, Dependency()]


class EmailService:
    """High-level email service with template rendering."""

    def __init__(
        self,
        email_client: BaseEmailClient,
        template_engine: JinjaTemplateEngine,
    ):
        self.client = email_client
        self.config = config
        self.template_engine = template_engine

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
    ) -> str:
        """Send an email using a named template. Returns message ID."""
        if isinstance(to, str):
            to = [to]

        to = [self.validate_email_address(email) for email in to]

        from_email = from_email or self.config.SES_FROM_EMAIL
        from_name = from_name or self.config.SES_FROM_NAME

        html_body, text_body = self.render_template(template_name, context)

        message = EmailMessage(
            to=to,
            subject=subject,
            body_html=html_body,
            body_text=text_body,
            from_email=from_email,
            from_name=from_name,
            reply_to=reply_to or self.config.SES_REPLY_TO_EMAIL,
        )

        return await self.client.send_email(message)

    async def send_magic_link_email(
        self,
        to_email: str,
        magic_link_url: str,
        expires_minutes: int = 15,
    ) -> str:
        """Send magic link login email."""
        return await self.send_email(
            to=to_email,
            subject="Sign in to Cuida",
            template_name="magic_link",
            context={
                "magic_link_url": magic_link_url,
                "expiration_minutes": expires_minutes,
            },
        )

    async def send_signup_confirmation_email(
        self,
        to_email: str,
    ) -> str:
        """Send welcome email after signup."""
        return await self.send_email(
            to=to_email,
            subject="Welcome to Cuida",
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
