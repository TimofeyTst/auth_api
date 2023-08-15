FROM python:3.10.9-slim-buster

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

RUN pip install -U pip && \
    pip install poetry

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

COPY pyproject.toml poetry.lock /tmp/

WORKDIR /tmp

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi --without prod

COPY . /src
ENV PATH "$PATH:/src/scripts"

ENV POETRY_CACHE_DIR /tmp/pypoetry

RUN useradd -m -d /src -s /bin/bash app \
    && chown -R app:app /src/* && chmod +x /src/scripts/*

WORKDIR /src
USER app

CMD ["./scripts/start-dev.sh"]
