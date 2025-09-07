# SRF Conference Insights
# Multi-stage build for optimal image size

# Build stage
FROM python:3.9-slim as builder

# Install system dependencies for building
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.9-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libmupdf-dev \
    libfreetype6-dev \
    libjpeg-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/app/.local

# Copy application code
COPY . .

# Change ownership of the app directory
RUN chown -R app:app /app

# Switch to app user
USER app

# Make sure scripts are in PATH
ENV PATH=/home/app/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Set default command
CMD ["python", "scripts/dev_server.py", "--host", "0.0.0.0", "--port", "8000"]

# Labels for better maintainability
LABEL maintainer="SRF Conference Insights Team"
LABEL description="AI-powered analysis platform for SRF conference papers"
LABEL version="1.0.0"
LABEL org.opencontainers.image.source="https://github.com/iuming/SRF_Conference_Insights"
