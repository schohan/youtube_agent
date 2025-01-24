FROM python:3.11-slim

RUN pip install poetry==1.6.1
RUN poetry config virtualenvs.create false


# create volumes
RUN mkdir -p /app/logs
RUN mkdir -p /app/data/raw
RUN mkdir -p /app/data/processed
RUN mkdir -p /app/data/test
RUN mkdir -p /app/data/models
RUN mkdir -p /app/data/models/llm
RUN mkdir -p /app/data/models/summarizer

# add new user
# ARG USER=mediauser
# RUN adduser --disabled-password --gecos "" $USER 
# USER $USER

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* ./README.md ./
COPY ./app ./app

RUN poetry install  --no-interaction --no-ansi

ENV PORT=${PORT:-8080}
EXPOSE ${PORT}

CMD ["poetry", "run", "uvicorn", "app.api.server:app", "--host", "0.0.0.0", "--port", "8080"]

