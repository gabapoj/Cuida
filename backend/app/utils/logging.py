import logging

from litestar.logging import LoggingConfig

from app.utils.configure import Config

logger = logging.getLogger(__name__)


class OTELTraceContextFilter(logging.Filter):
    """Inject OpenTelemetry trace_id and span_id into every log record.

    Enables correlation between logs and distributed traces in BetterStack.
    Gracefully sets both fields to None if OTEL is not active.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            from opentelemetry import trace  # noqa: PLC0415

            span = trace.get_current_span()
            if span and span.get_span_context().is_valid:
                ctx = span.get_span_context()
                record.trace_id = format(ctx.trace_id, "032x")  # type: ignore[attr-defined]
                record.span_id = format(ctx.span_id, "016x")  # type: ignore[attr-defined]
            else:
                record.trace_id = None  # type: ignore[attr-defined]
                record.span_id = None  # type: ignore[attr-defined]
        except ImportError:
            record.trace_id = None  # type: ignore[attr-defined]
            record.span_id = None  # type: ignore[attr-defined]
        return True


def create_logging_config(config: Config) -> LoggingConfig:
    """Return a Litestar LoggingConfig suited to the environment.

    Development:  Rich console output with tracebacks and trace context.
    Production:   Structured text with trace_id/span_id for BetterStack correlation.
    """
    if config.IS_DEV:
        return LoggingConfig(
            configure_root_logger=not config.OTEL_ENABLED,
            filters={
                "otel_trace_context": {
                    "()": "app.utils.logging.OTELTraceContextFilter",
                },
            },
            handlers={
                "console": {
                    "class": "rich.logging.RichHandler",
                    "filters": ["otel_trace_context"],
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
            configure_root_logger=not config.OTEL_ENABLED,
            filters={
                "otel_trace_context": {
                    "()": "app.utils.logging.OTELTraceContextFilter",
                },
            },
            formatters={
                "production": {
                    "format": (
                        "%(asctime)s [%(levelname)s] %(name)s - %(message)s | trace_id=%(trace_id)s span_id=%(span_id)s"
                    ),
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            handlers={
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "production",
                    "filters": ["otel_trace_context"],
                    "level": config.LOG_LEVEL,
                },
            },
            loggers={
                "uvicorn.access": {"level": "WARNING"},
            },
        )
