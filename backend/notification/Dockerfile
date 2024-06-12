FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

WORKDIR /app/backend/

COPY pyproject.toml /app/
COPY poetry.lock /app/ 

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

RUN mkdir -p /app/backend/notification/notification && chmod -R 777 /app/backend/notification/notification

COPY . /app/backend

ENV PYTHONPATH=/app/backend

EXPOSE 8001

CMD ["uvicorn", "notification.notification_main:notification_app", "--host", "0.0.0.0", "--port", "8004", "--ssl-certfile", "/certs/cert.pem", "--ssl-keyfile", "/certs/key.pem"]

