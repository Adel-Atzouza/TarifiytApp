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
        unixodbc \
        unixodbc-dev \
        gnupg \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18 \
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
COPY ./src /app/src
COPY ./scripts /app/scripts
COPY ./migrations /app/migrations

# Install optional dev dependencies
ARG INSTALL_DEV=false
RUN --mount=type=cache,target=/root/.cache/uv \
    if [ "$INSTALL_DEV" = "true" ]; then \
        echo "Installing with dev dependencies"; \
        uv sync --frozen --no-install-project --extra dev; \
    else \
        echo "Installing without dev dependencies"; \
        uv sync --frozen --no-install-project --no-dev; \
    fi

CMD ["make", "run"]