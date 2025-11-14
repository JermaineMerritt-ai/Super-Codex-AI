# Super-Codex-AI RAG System Dockerfile
# Multi-stage build for production-ready deployment

# ============================================================================
# Base Python Image
# ============================================================================
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.6.1

# ============================================================================
# Dependencies Stage
# ============================================================================
FROM base as dependencies

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-root \
    && rm -rf $POETRY_CACHE_DIR

# ============================================================================
# Development Stage
# ============================================================================
FROM dependencies as development

# Install development dependencies
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

# Create app directory
WORKDIR /app

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/data/corpus \
    && mkdir -p /app/data/vectors \
    && mkdir -p /app/logs \
    && mkdir -p /app/config \
    && mkdir -p /app/artifacts

# Set proper permissions
RUN chmod +x /app/ops/scripts/*.ps1 2>/dev/null || true

# Expose application port
EXPOSE 8000

# Development command
CMD ["uvicorn", "engine.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================================================
# Production Stage
# ============================================================================
FROM dependencies as production

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Create app directory
WORKDIR /app

# Copy application code (excluding development files)
COPY --chown=appuser:appuser engine/ ./engine/
COPY --chown=appuser:appuser scrolls/ ./scrolls/
COPY --chown=appuser:appuser ops/scripts/ ./ops/scripts/
COPY --chown=appuser:appuser pyproject.toml ./

# Create data directories with proper ownership
RUN mkdir -p /app/data/corpus \
    && mkdir -p /app/data/vectors \
    && mkdir -p /app/logs \
    && mkdir -p /app/config \
    && mkdir -p /app/artifacts \
    && chown -R appuser:appuser /app

# Install the application
RUN poetry install --no-dev --no-root

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose application port
EXPOSE 8000

# Production command
CMD ["uvicorn", "engine.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# ============================================================================
# Testing Stage
# ============================================================================
FROM development as testing

# Install additional testing dependencies
RUN pip install pytest pytest-asyncio pytest-cov httpx

# Copy test files
COPY tests/ ./tests/

# Run tests by default
CMD ["pytest", "-v", "--cov=engine", "--cov=scrolls", "tests/"]

# ============================================================================
# Build Arguments and Labels
# ============================================================================
ARG BUILD_VERSION=unknown
ARG BUILD_DATE=unknown
ARG GIT_COMMIT=unknown

LABEL maintainer="Super-Codex-AI Team" \
      version="${BUILD_VERSION}" \
      build_date="${BUILD_DATE}" \
      git_commit="${GIT_COMMIT}" \
      description="Super-Codex-AI RAG System with Ceremonial Scroll Generation" \
      org.opencontainers.image.title="Super-Codex-AI Codex System" \
      org.opencontainers.image.description="Advanced RAG system with scroll templating and ceremonial governance" \
      org.opencontainers.image.version="${BUILD_VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.revision="${GIT_COMMIT}" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/your-org/super-codex-ai"