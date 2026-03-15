from enum import StrEnum, auto


class TaskName(StrEnum):
    SEND_EMAIL = auto()
    HEALTH_CHECK = auto()


class TaskStatus(StrEnum):
    PENDING = auto()
    ACTIVE = auto()
    COMPLETE = auto()
    FAILED = auto()
    ABORTED = auto()
