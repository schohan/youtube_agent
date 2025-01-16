FROM python:3.11-slim

RUN pip install poetry==1.6.1

RUN poetry config virtualenvs.create false

WORKDIR /code

COPY ./pyproject.toml ./README.md ./poetry.lock* ./

COPY ./package[s] ./packages

RUN poetry install  --no-interaction --no-ansi --no-root

COPY ./youtube_agent ./youtube_agent

RUN poetry install --no-interaction --no-ansi

EXPOSE 8080

CMD exec uvicorn youtube_agent.api.server:app --host 0.0.0.0 --port 8080

