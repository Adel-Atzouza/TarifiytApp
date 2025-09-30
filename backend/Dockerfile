FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies including ODBC drivers for MSSQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        make \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Prepare UV
COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependencies before installation
COPY pyproject.toml uv.lock alembic.ini /app/
COPY Makefile /app/
COPY ./api /app/api
COPY ./scripts /app/scripts
COPY ./migrations /app/migrations

# Install optional dev dependencies
ARG INSTALL_DEV=true
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ "$INSTALL_DEV" = "true" ]; then \
        echo "Installing with dev dependencies"; \
        uv sync --locked --extra dev; \
    else \
        echo "Installing without dev dependencies"; \
        uv sync --locked --no-dev; \
    fi

CMD ["make", "run"]