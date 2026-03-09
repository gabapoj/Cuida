"""OpenTelemetry initialization for BetterStack OTLP integration.

Sets up full observability (logs + traces + metrics) using native Litestar patterns
and OpenTelemetry SDK defaults. All exports are non-blocking via batch processors
and fail gracefully if BetterStack is unavailable.
"""

import logging
import sys

from opentelemetry import metrics, trace  # type: ignore[import-untyped]
from opentelemetry._logs import set_logger_provider  # type: ignore[import-untyped]
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter  # type: ignore[import-untyped]
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter  # type: ignore[import-untyped]
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter  # type: ignore[import-untyped]
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor  # type: ignore[import-untyped]
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor  # type: ignore[import-untyped]
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler  # type: ignore[import-untyped]
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor  # type: ignore[import-untyped]
from opentelemetry.sdk.metrics import MeterProvider  # type: ignore[import-untyped]
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader  # type: ignore[import-untyped]
from opentelemetry.sdk.resources import Resource  # type: ignore[import-untyped]
from opentelemetry.sdk.trace import TracerProvider  # type: ignore[import-untyped]
from opentelemetry.sdk.trace.export import BatchSpanProcessor  # type: ignore[import-untyped]

from app.utils.configure import ConfigProtocol

logger = logging.getLogger(__name__)

# Global references for shutdown
_tracer_provider: TracerProvider | None = None
_meter_provider: MeterProvider | None = None
_logger_provider: LoggerProvider | None = None


def create_resource(config: ConfigProtocol) -> Resource:
    return Resource.create(
        {
            "service.name": config.OTEL_SERVICE_NAME,
            "service.version": config.OTEL_SERVICE_VERSION,
            "deployment.environment": config.ENV,
        }
    )


def setup_tracing(config: ConfigProtocol, resource: Resource) -> TracerProvider | None:
    if not config.BETTERSTACK_OTLP_INGESTING_HOST or not config.BETTERSTACK_OTLP_SOURCE_TOKEN:
        logger.warning("BetterStack credentials not configured. Skipping trace export.")
        return None

    try:
        span_exporter = OTLPSpanExporter(
            endpoint=f"https://{config.BETTERSTACK_OTLP_INGESTING_HOST}/v1/traces",
            headers={"Authorization": f"Bearer {config.BETTERSTACK_OTLP_SOURCE_TOKEN}"},
        )
        tracer_provider = TracerProvider(resource=resource)
        tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
        trace.set_tracer_provider(tracer_provider)
        logger.info("OpenTelemetry tracing initialized (exporting to BetterStack)")
        return tracer_provider
    except Exception as e:
        logger.error(f"Failed to initialize OpenTelemetry tracing: {e}", exc_info=True)
        return None


def setup_metrics(config: ConfigProtocol, resource: Resource) -> MeterProvider | None:
    if not config.BETTERSTACK_OTLP_INGESTING_HOST or not config.BETTERSTACK_OTLP_SOURCE_TOKEN:
        logger.warning("BetterStack credentials not configured. Skipping metrics export.")
        return None

    try:
        metric_exporter = OTLPMetricExporter(
            endpoint=f"https://{config.BETTERSTACK_OTLP_INGESTING_HOST}/v1/metrics",
            headers={"Authorization": f"Bearer {config.BETTERSTACK_OTLP_SOURCE_TOKEN}"},
        )
        meter_provider = MeterProvider(
            resource=resource,
            metric_readers=[PeriodicExportingMetricReader(metric_exporter)],
        )
        metrics.set_meter_provider(meter_provider)
        logger.info("OpenTelemetry metrics initialized (exporting to BetterStack)")
        return meter_provider
    except Exception as e:
        logger.error(f"Failed to initialize OpenTelemetry metrics: {e}", exc_info=True)
        return None


def setup_logging(config: ConfigProtocol, resource: Resource) -> LoggerProvider | None:
    if not config.BETTERSTACK_OTLP_INGESTING_HOST or not config.BETTERSTACK_OTLP_SOURCE_TOKEN:
        logger.warning("BetterStack credentials not configured. Skipping log export.")
        return None

    try:
        log_exporter = OTLPLogExporter(
            endpoint=f"https://{config.BETTERSTACK_OTLP_INGESTING_HOST}/v1/logs",
            headers={"Authorization": f"Bearer {config.BETTERSTACK_OTLP_SOURCE_TOKEN}"},
        )
        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        set_logger_provider(logger_provider)
        # Bridge stdlib logging → OTLP export (runs in parallel with stdout logging)
        handler = LoggingHandler(logger_provider=logger_provider)
        logging.getLogger().addHandler(handler)
        logger.info("OpenTelemetry logging initialized (exporting to BetterStack)")
        return logger_provider
    except Exception as e:
        logger.error(f"Failed to initialize OpenTelemetry logging: {e}", exc_info=True)
        return None


def setup_instrumentation() -> None:
    try:
        SQLAlchemyInstrumentor().instrument()
        HTTPXClientInstrumentor().instrument()
        logger.info("Auto-instrumentation enabled (SQLAlchemy, httpx)")
    except Exception as e:
        logger.error(f"Failed to enable auto-instrumentation: {e}", exc_info=True)


def initialize_opentelemetry(config: ConfigProtocol) -> None:
    """Main entry point called by factory.py before creating the Litestar app."""
    global _tracer_provider, _meter_provider, _logger_provider

    if not config.OTEL_ENABLED:
        logger.info("OpenTelemetry disabled (no BetterStack credentials)")
        return

    logger.info(f"Initializing OpenTelemetry for service: {config.OTEL_SERVICE_NAME}")

    try:
        resource = create_resource(config)
        _tracer_provider = setup_tracing(config, resource)
        _meter_provider = setup_metrics(config, resource)
        _logger_provider = setup_logging(config, resource)
        setup_instrumentation()
        logger.info("OpenTelemetry initialization complete")
    except Exception as e:
        logger.error(f"Failed to initialize OpenTelemetry: {e}", exc_info=True)
        sys.stderr.write(f"ERROR: OpenTelemetry initialization failed: {e}\n")


def shutdown_opentelemetry() -> None:
    """Flush and shut down all OTEL providers. Called via Litestar on_shutdown."""
    global _tracer_provider, _meter_provider, _logger_provider

    logger.info("Shutting down OpenTelemetry...")

    try:
        if _tracer_provider:
            _tracer_provider.shutdown()
        if _meter_provider:
            _meter_provider.shutdown()
        if _logger_provider:
            _logger_provider.shutdown()
    except Exception as e:
        logger.error(f"Error during OpenTelemetry shutdown: {e}", exc_info=True)
        sys.stderr.write(f"ERROR: OpenTelemetry shutdown failed: {e}\n")
