from enum import StrEnum


class CalendarEventType(StrEnum):
    VISIT = "visit"
    APPOINTMENT = "appointment"
    OTHER = "other"
