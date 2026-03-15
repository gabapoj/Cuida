from enum import StrEnum, auto


class CalendarEventType(StrEnum):
    VISIT = auto()
    APPOINTMENT = auto()
    OTHER = auto()
