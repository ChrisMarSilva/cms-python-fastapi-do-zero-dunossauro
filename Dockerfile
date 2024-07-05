FROM python:3.12.4-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

## Primeira fase: Base
#FROM python:3.12.4-slim-buster AS base
#WORKDIR /code
#COPY requirements.txt /code/
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
## Segunda fase: Builder
#FROM base AS builder
#COPY . /code/
## Terceira fase: Runtime
#FROM base AS runtime
#COPY --from=builder /code/ /code/
#EXPOSE 8000
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


## Primeira fase: Base
#FROM python:3.12.4-slim-buster AS base
#WORKDIR /code
#COPY requirements.txt /code/
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
#
## Segunda fase: Builder
#FROM base AS builder
#COPY . /code/
#
## Fase de Teste
#FROM builder AS test
#RUN pip install pytest
#RUN pytest
#
## Terceira fase: Runtime
#FROM base AS runtime
#COPY --from=builder /code/ /code/
#EXPOSE 8000
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


#FROM python:3.12-bullseye
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#RUN mkdir /src
#COPY . /src
#WORKDIR /src
#EXPOSE 8000
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10
#WORKDIR /app/
#RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && cd /usr/local/bin && ln -s /opt/poetry/bin/poetry && poetry config virtualenvs.create false
#COPY ./pyproject.toml ./poetry.lock* /app/
#ARG INSTALL_DEV=false
#RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"
#ENV PYTHONPATH=/app
#COPY ./scripts/ /app/
#COPY ./alembic.ini /app/
#COPY ./prestart.sh /app/
#COPY ./tests-start.sh /app/
#COPY ./app /app/app
