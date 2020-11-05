FROM python:3.9-slim
LABEL  maintainer "nukopy <pytwbf201830@gmail.com>"

WORKDIR /opt/python
ENV PYTHONPATH "/opt/python"

# install packages
RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        zip \
        libsnappy-dev \
    && pip install -U --no-cache-dir poetry \
    && rm -rf /var/lib/apt/lists/*

# install Python packages
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install
COPY ./app /opt/python/app

ENV PYTHONPATH "/opt/python"