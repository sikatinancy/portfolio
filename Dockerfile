FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY nancy_portfolio/requirements.txt ./nancy_portfolio/requirements.txt
RUN pip install --upgrade pip && pip install -r ./nancy_portfolio/requirements.txt

COPY nancy_portfolio/ ./nancy_portfolio/

WORKDIR /app/nancy_portfolio
ENV DJANGO_SETTINGS_MODULE=config.settings.production

EXPOSE 8000

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8000} config.wsgi:application"]
