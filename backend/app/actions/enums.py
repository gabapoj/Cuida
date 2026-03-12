from enum import StrEnum, auto


class ActionGroupType(StrEnum):
    """Types of action groups. Add domain action groups here as they are implemented."""

    UserActions = "user_actions"


class ActionResultType(StrEnum):
    """Types of actions the frontend should take after action execution."""

    redirect = "redirect"
    download_file = "download_file"


class ActionIcon(StrEnum):
    default = auto()
    refresh = auto()
    download = auto()
    send = auto()
    edit = auto()
    trash = auto()
    add = auto()
    check = auto()
    x = auto()
