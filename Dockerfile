FROM python:3.11-slim

# For live reload
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY src/ ./src/

ENV HUD_LOG_STREAM=stderr

RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir -e .

CMD ["sh", "-c", "\
    python -m hud_controller.context >&2 & \
    exec python -m hud_controller.server \
"]