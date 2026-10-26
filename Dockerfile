# Stage 1: Build & Dependencies stage
FROM python:3.10-slim AS builder

WORKDIR /build

# Install build dependencies if needed
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Minimal Production Runtime
FROM python:3.10-slim AS runtime

# Set environment variables for production security and Python performance
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    APP_VERSION=1.0.0 \
    PATH="/home/appuser/.local/bin:$PATH"

# Create non-root system group and user
RUN groupadd -r -g 1000 appgroup && \
    useradd -r -u 1000 -g appgroup -m -d /home/appuser -s /sbin/nologin appuser

WORKDIR /app

# Copy installed python packages from builder stage
COPY --from=builder --chown=appuser:appgroup /root/.local /home/appuser/.local

# Copy application source code and web assets
COPY --chown=appuser:appgroup app.py .
COPY --chown=appuser:appgroup templates/ templates/

# Switch to unprivileged non-root user
USER 1000:1000

# Expose application port
EXPOSE 5000

# Container healthcheck using standard Python library
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, os; urllib.request.urlopen(f'http://127.0.0.1:{os.environ.get(\"PORT\", 5000)}/health')" || exit 1

# Start Flask application
CMD ["python", "app.py"]
