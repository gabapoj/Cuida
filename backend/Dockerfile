FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install dependencies before copying source (better layer caching once uv.lock exists)
# When uv.lock is committed, replace the RUN below with:
#   COPY pyproject.toml uv.lock ./
#   RUN uv sync --frozen --no-dev --no-install-project
COPY pyproject.toml ./
RUN uv sync --no-dev --no-install-project

# Copy application source
COPY . .

# Install the project itself
RUN uv sync --no-dev

ENV PATH="/app/.venv/bin:$PATH"

# Production: run migrations then start server
# For ECS, use scripts/start.sh which runs alembic first
CMD ["uvicorn", "app.index:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
