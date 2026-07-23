FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim AS runtime
RUN useradd -m -u 1000 appuser
COPY --from=builder /install /usr/local
WORKDIR /app
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser .env ./

USER appuser
ENV PYTHONPATH=/app/src
ENTRYPOINT ["python", "-m", "ai_agent.cli.main"]
