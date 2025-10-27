# ========================================
# Backend Dockerfile - FastAPI con UV
# ========================================

FROM python:3.12-slim AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    redis-tools \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

# Copiar archivos de dependencias
COPY pyproject.toml ./
COPY uv.lock ./

# Instalar UV y dependencias
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Exportar e instalar dependencias
RUN uv export --no-hashes > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Establecer directorio de trabajo
WORKDIR /app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:9000/ping || exit 1

EXPOSE 8000

# Comando por defecto (será sobrescrito por docker-compose)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]