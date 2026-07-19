FROM python:3.12-slim-bookworm

LABEL org.opencontainers.image.title="KES Water API"
LABEL org.opencontainers.image.description="Enterprise Water Engineering Platform by Kamra Engineering Solutions"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN groupadd --system keswater \
    && useradd --system --gid keswater --home-dir /app keswater

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --requirement /app/requirements.txt

COPY --chown=keswater:keswater app /app/app
COPY --chown=keswater:keswater alembic /app/alembic
COPY --chown=keswater:keswater alembic.ini /app/alembic.ini

RUN mkdir -p /app/logs \
    && chown -R keswater:keswater /app/logs

USER keswater

EXPOSE 8010

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8010/api/v1/health', timeout=3)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]