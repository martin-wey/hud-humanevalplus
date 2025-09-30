FROM python:3.11-slim

# For live reload
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml ./
COPY src/ ./src/

ENV HUD_LOG_STREAM=stderr

RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir -e .

CMD ["python", "-m", "hud_controller.server"]
