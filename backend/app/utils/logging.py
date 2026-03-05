import logging

from litestar.logging import LoggingConfig

from app.utils.configure import Config

logger = logging.getLogger(__name__)


def create_logging_config(config: Config) -> LoggingConfig:
    """Return a Litestar LoggingConfig suited to the environment.

    Development:  Rich console output with tracebacks and local variable display.
    Production:   Structured text with timestamp, level, and logger name.
    """
    if config.IS_DEV:
        return LoggingConfig(
            handlers={
                "console": {
                    "class": "rich.logging.RichHandler",
                    "rich_tracebacks": True,
                    "tracebacks_suppress": ["litestar", "starlette", "uvicorn", "anyio"],
                    "tracebacks_show_locals": True,
                    "markup": False,
                    "show_time": False,
                    "show_level": True,
                    "show_path": True,
                },
            },
            loggers={
                "uvicorn.access": {"level": "WARNING"},
            },
        )
    else:
        return LoggingConfig(
            formatters={
                "production": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            handlers={
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "production",
                    "level": config.LOG_LEVEL,
                },
            },
            loggers={
                "uvicorn.access": {"level": "WARNING"},
            },
        )
