FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV MODULE_NAME="raddar.main"

WORKDIR /raddar/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /raddar/

RUN poetry install --no-root --no-dev && \
    mkdir /raddar/results

COPY ./raddar /raddar/raddar/
ENV PYTHONPATH=/raddar