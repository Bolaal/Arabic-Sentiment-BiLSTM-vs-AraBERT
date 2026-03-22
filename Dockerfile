# Multi-stage Dockerfile for Arabic Sentiment Analysis API
# Optimized for production deployment with small image size

# ================================
# Stage 1: Builder
# ================================
FROM python:3.11-slim-bookworm AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        g++ && \
    rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r /tmp/requirements.txt

# ================================
# Stage 2: Runtime
# ================================
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    MODEL_NAME="Belall87/arabert-arabic-sentiment" \
    PORT=8000 \
    WORKERS=1 \
    LOG_LEVEL=info \
    MAX_LENGTH=128 \
    CORS_ORIGINS="*"

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=appuser:appuser backend/main.py /app/

# Switch to non-root user
USER appuser

# Create cache directory for Hugging Face models
RUN mkdir -p /home/appuser/.cache/huggingface

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
   CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers ${WORKERS} --log-level ${LOG_LEVEL}"]