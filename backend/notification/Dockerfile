FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml /app/
COPY poetry.lock /app/ 

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "notification_main:notification_app", "--host", "0.0.0.0", "--port", "8000"]

