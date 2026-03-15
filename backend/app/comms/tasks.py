"""Comms async tasks."""

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.comms.clients.email import BaseEmailClient, EmailPayload, EmailSendError
from app.comms.enums import EmailMessageStatus
from app.comms.models.emails import EmailMessage
from app.queue.registry import TaskName, task
from app.queue.transactions import with_transaction
from app.queue.types import AppContext


@task(TaskName.SEND_EMAIL)
@with_transaction
async def send_email_task(
    ctx: AppContext,
    *,
    transaction: AsyncSession,
    email_client: BaseEmailClient,
    email_message_id: int,
) -> None:
    """Send a queued email and update its status in the DB.

    On success: marks SENT + records ses_message_id + sent_at.
    On failure: raises EmailSendError (a CommittableTaskException), which causes
    with_transaction to commit the FAILED status before re-raising for SAQ to retry.
    """
    record = await transaction.get(EmailMessage, email_message_id)
    if record is None:
        raise ValueError(f"EmailMessage {email_message_id} not found")

    payload = EmailPayload(
        to=record.to_email,
        subject=record.subject,
        body_html=record.body_html,
        body_text=record.body_text,
        from_email=record.from_email,
        from_name=record.from_name,
        reply_to=record.reply_to_email,
    )

    try:
        message_id = await email_client.send_email(payload)
        record.ses_message_id = message_id
        record.status = EmailMessageStatus.SENT
        record.sent_at = datetime.now(UTC)
    except Exception as e:
        record.status = EmailMessageStatus.FAILED
        record.error_message = str(e)
        raise EmailSendError(str(e)) from e
