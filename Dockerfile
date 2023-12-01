FROM python:3.10.0-slim-buster as base

ENV \
  PYTHONFAULTHANDLER=TRUE \
  PYTHONUNBUFFERED=TRUE \
  POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_IN_PROJECT=true \
  POETRY_NO_INTERACTION=1 \
  PYSETUP_PATH="/opt/pysetup" \
  VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base as builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ gettext libpq-dev curl

ARG POETRY_VERSION="1.3.2"
RUN curl -sSL https://install.python-poetry.org | python -

WORKDIR $PYSETUP_PATH

COPY pyproject.toml poetry.lock ./

RUN poetry install -vvv --no-root

COPY toubib toubib
COPY tests tests

RUN poetry install

FROM base as final

WORKDIR $PYSETUP_PATH

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /data
VOLUME /data

COPY --from=builder $VENV_PATH $VENV_PATH
COPY toubib toubib
COPY tests tests
COPY setup.cfg setup.cfg
COPY alembic.ini alembic.ini

ENV PORT 8000
ENV sqlalchemy_url sqlite:////data/db.sqlite?check_same_thread=false
EXPOSE ${PORT}

CMD exec hypercorn toubib.main:app --workers 1 --graceful-timeout 30 --bind 0.0.0.0:${PORT}
