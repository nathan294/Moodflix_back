ARG VERSION
FROM python:$VERSION
ARG UID
WORKDIR /app

ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on

RUN useradd -u $UID -s /bin/bash -d /app techdata-user \
    && chown -R techdata-user: /app
USER techdata-user


RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/app/.local/bin:${PATH}"


ENTRYPOINT []
