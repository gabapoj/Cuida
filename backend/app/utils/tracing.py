"""Explicit tracing decorator for business logic operations."""

import logging
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from opentelemetry import trace
from opentelemetry.trace import Span

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


type SpanEnricher = Callable[[Span, Any, Any], None]


def trace_operation[T](
    operation_name: str,
    *,
    enrich: SpanEnricher | None = None,
) -> Callable[[Callable[..., Awaitable[T]]], Callable[..., Awaitable[T]]]:
    """Trace async operations with an explicit operation name and optional span enrichment.

    Usage:
        @trace_operation("user_create")
        async def create_user(name: str) -> User:
            ...

        def enrich_span(span: Span, args: tuple, kwargs: dict) -> None:
            span.set_attribute("user.id", kwargs.get("user_id"))

        @trace_operation("call_start", enrich=enrich_span)
        async def start_call(self, user_id: int) -> Call:
            ...
    """

    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            with tracer.start_as_current_span(operation_name) as span:
                span.set_attribute("code.function", func.__qualname__)
                span.set_attribute("code.namespace", func.__module__)

                if enrich and span.is_recording():
                    try:
                        enrich(span, args, kwargs)
                    except Exception as e:
                        logger.debug(f"Span enrichment failed: {e}", exc_info=True)

                try:
                    result = await func(*args, **kwargs)
                    span.set_attribute("operation.status", "success")
                    return result
                except Exception as e:
                    span.set_attribute("operation.status", "error")
                    span.record_exception(e)
                    raise

        return wrapper

    return decorator


def get_trace_context() -> dict[str, str]:
    """Get current trace_id and span_id for manual log correlation."""
    span = trace.get_current_span()
    if not span:
        return {"trace_id": "", "span_id": ""}

    ctx = span.get_span_context()
    if not ctx.is_valid:
        return {"trace_id": "", "span_id": ""}

    return {
        "trace_id": format(ctx.trace_id, "032x"),
        "span_id": format(ctx.span_id, "016x"),
    }
