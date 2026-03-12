from enum import StrEnum


class ContactType(StrEnum):
    PHONE = "phone"
    EMAIL = "email"


class Direction(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class TextMessageStatus(StrEnum):
    QUEUED = "queued"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    RECEIVED = "received"


class PhoneCallStatus(StrEnum):
    INITIATED = "initiated"
    RINGING = "ringing"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    NO_ANSWER = "no_answer"
    BUSY = "busy"
