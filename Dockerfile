# Use official lightweight Python base image
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_VERSION=1.0.0

# Set working directory
WORKDIR /app

# Create a non-root system user for security best practices
RUN groupadd -r appuser && useradd -r -g appuser -u 1000 appuser

# Copy requirements first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and templates
COPY app.py .
COPY templates/ templates/

# Set appropriate ownership and switch to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Expose container port
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
