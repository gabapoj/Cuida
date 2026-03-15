from enum import StrEnum, auto


class TaskName(StrEnum):
    SEND_EMAIL = auto()
    HEALTH_CHECK = auto()
