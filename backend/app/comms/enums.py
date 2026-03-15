from enum import StrEnum, auto


class EmailMessageStatus(StrEnum):
    PENDING = auto()
    SENT = auto()
    FAILED = auto()


class ContactType(StrEnum):
    PHONE = auto()
    EMAIL = auto()


class Direction(StrEnum):
    INBOUND = auto()
    OUTBOUND = auto()


class TextMessageStatus(StrEnum):
    QUEUED = auto()
    SENT = auto()
    DELIVERED = auto()
    FAILED = auto()
    RECEIVED = auto()


class PhoneCallStatus(StrEnum):
    INITIATED = auto()
    RINGING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()
    NO_ANSWER = auto()
    BUSY = auto()
