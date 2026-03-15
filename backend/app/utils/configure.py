import json
import logging
import os
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

import boto3
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load .env.local from the backend working directory (or project root if running from there)
load_dotenv(".env.local")
load_dotenv("../.env.local")  # fallback when running from project root

# Load secrets from AWS Secrets Manager if running in AWS
secret_arn = os.getenv("APP_SECRETS_ARN")
if secret_arn:
    _client = boto3.client("secretsmanager")
    _response = _client.get_secret_value(SecretId=secret_arn)
    _secrets = json.loads(_response["SecretString"])
    for _key, _value in _secrets.items():
        if _value:
            os.environ[_key] = _value
    logger.info(f"Loaded {len(_secrets)} secrets from AWS Secrets Manager")


@runtime_checkable
class ConfigProtocol(Protocol):
    """Minimal config interface used for type-safe dependency injection."""

    SECRET_KEY: str
    FRONTEND_ORIGIN: str
    SES_REGION: str
    SES_FROM_NAME: str
    SES_FROM_EMAIL: str
    SES_REPLY_TO_EMAIL: str
    LOG_LEVEL: str
    BETTERSTACK_OTLP_INGESTING_HOST: str
    BETTERSTACK_OTLP_SOURCE_TOKEN: str

    ENV: str

    @property
    def IS_DEV(self) -> bool: ...

    @property
    def ALLOW_LOCAL_SES(self) -> bool: ...

    @property
    def QUEUE_SYNC(self) -> bool: ...

    @property
    def SES_CONFIGURATION_SET(self) -> str: ...

    @property
    def OTEL_ENABLED(self) -> bool: ...

    @property
    def OTEL_SERVICE_NAME(self) -> str: ...

    @property
    def OTEL_SERVICE_VERSION(self) -> str: ...


@dataclass
class Config:
    """Application configuration — reads from environment variables."""

    # ─── App ──────────────────────────────────────────────────────────────────
    ENV: str = os.getenv("ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # ─── CORS ─────────────────────────────────────────────────────────────────
    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    SUCCESS_REDIRECT_URL: str = os.getenv("SUCCESS_REDIRECT_URL", os.getenv("FRONTEND_ORIGIN", "http://localhost:5173"))
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")

    # ─── Redis ────────────────────────────────────────────────────────────────
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # ─── Email (AWS SES) ──────────────────────────────────────────────────────
    SES_REGION: str = os.getenv("SES_REGION", "us-east-1")
    SES_FROM_NAME: str = os.getenv("SES_FROM_NAME", "Cuida")
    SES_FROM_EMAIL: str = os.getenv("SES_FROM_EMAIL", "noreply@cuida.app")
    SES_REPLY_TO_EMAIL: str = os.getenv("SES_REPLY_TO_EMAIL", "support@cuida.app")
    EMAIL_TEMPLATES_DIR: str = "templates/emails-react"
    _allow_local_ses: str = os.getenv("ALLOW_LOCAL_SES", "false")
    _queue_sync: str | None = os.getenv("QUEUE_SYNC", "false")

    @property
    def ALLOW_LOCAL_SES(self) -> bool:
        return self._allow_local_ses.lower() == "true"

    @property
    def QUEUE_SYNC(self) -> bool:
        if self.IS_DEV and self._queue_sync:
            return self._queue_sync.lower() == "true"
        return False

    # ─── Observability (BetterStack / OpenTelemetry) ──────────────────────────
    BETTERSTACK_OTLP_INGESTING_HOST: str = os.getenv("BETTERSTACK_OTLP_INGESTING_HOST", "")
    BETTERSTACK_OTLP_SOURCE_TOKEN: str = os.getenv("BETTERSTACK_OTLP_SOURCE_TOKEN", "")

    # ─── Phase 3: Provider flags ───────────────────────────────────────────────
    # Switching providers = one env var change (see app/llm/, app/voice/, app/telephony/)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    STT_PROVIDER: str = os.getenv("STT_PROVIDER", "deepgram")
    TTS_PROVIDER: str = os.getenv("TTS_PROVIDER", "elevenlabs")
    TELEPHONY_PROVIDER: str = os.getenv("TELEPHONY_PROVIDER", "telnyx")

    # ─── Computed properties ───────────────────────────────────────────────────

    @property
    def IS_DEV(self) -> bool:
        return self.ENV == "development"

    @property
    def OTEL_ENABLED(self) -> bool:
        """Enable OpenTelemetry if BetterStack credentials are configured."""
        return bool(self.BETTERSTACK_OTLP_INGESTING_HOST and self.BETTERSTACK_OTLP_SOURCE_TOKEN)

    @property
    def OTEL_SERVICE_NAME(self) -> str:
        return f"cuida-backend-{self.ENV}"

    @property
    def OTEL_SERVICE_VERSION(self) -> str:
        return "0.1.0"

    @property
    def SES_CONFIGURATION_SET(self) -> str:
        """SES configuration set — override via env var or derive from ALLOW_LOCAL_SES."""
        if config_set := os.getenv("SES_CONFIGURATION_SET"):
            return config_set
        return "cuida-production-ses" if self.ALLOW_LOCAL_SES or not self.IS_DEV else "cuida-dev-ses"

    def _build_db_url(
        self,
        driver: str = "",
        user: str | None = None,
        password: str | None = None,
        port: str | None = None,
    ) -> str:
        endpoint = os.getenv("DB_ENDPOINT", "localhost")
        port = port or os.getenv("DB_PORT", "5432")
        name = os.getenv("DB_NAME", "cuida")
        user = user or os.getenv("DB_USER", "postgres")
        password = password or os.getenv("DB_PASSWORD", "postgres")
        protocol = f"postgresql{driver}"
        return f"{protocol}://{user}:{password}@{endpoint}:{port}/{name}"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        """Async SQLAlchemy URL (psycopg3 driver) — used by the app at runtime."""
        if url := os.getenv("ASYNC_DATABASE_URL"):
            return url
        return self._build_db_url(driver="+psycopg")

    @property
    def ADMIN_DB_URL(self) -> str:
        """Sync PostgreSQL URL — used by Alembic for migrations."""
        if url := os.getenv("ADMIN_DB_URL"):
            return url
        admin_user = os.getenv("DB_ADMIN_USER", "postgres")
        admin_password = os.getenv("DB_ADMIN_PASSWORD", "postgres")
        return self._build_db_url(user=admin_user, password=admin_password)


@dataclass
class DevelopmentConfig(Config):
    """Development environment configuration."""

    ENV: str = "development"


@dataclass
class ProductionConfig(Config):
    """Production environment configuration."""

    ENV: str = "production"


@dataclass
class TestConfig(Config):
    """Test environment — points at the test database on port 5433."""

    __test__ = False  # Prevent pytest from collecting this as a test class

    ENV: str = "testing"

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        if url := os.getenv("TEST_ASYNC_DATABASE_URL") or os.getenv("ASYNC_DATABASE_URL"):
            return url
        return self._build_db_url(driver="+psycopg", port="5433")

    @property
    def ADMIN_DB_URL(self) -> str:
        if url := os.getenv("TEST_ADMIN_DB_URL") or os.getenv("ADMIN_DB_URL"):
            return url
        return self._build_db_url(port="5433")


def get_config() -> Config:
    env = os.getenv("ENV", "development")
    if env == "testing":
        return TestConfig()
    elif env == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig()


# Global singleton — imported by factory.py and alembic/env.py
config = get_config()
