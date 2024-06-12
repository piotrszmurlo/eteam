FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app

EXPOSE 8003

CMD ["uvicorn", "payment_main:payment_app", "--host", "0.0.0.0", "--port", "8003"]


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

WORKDIR /app/backend/

COPY pyproject.toml /app/
COPY poetry.lock /app/ 

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

RUN mkdir -p /app/backend/payment/payment && chmod -R 777 /app/backend/payment/payment

COPY . /app/backend

ENV PYTHONPATH=/app/backend

EXPOSE 8001

CMD ["uvicorn", "payment.payment_main:payment_app", "--host", "0.0.0.0", "--port", "8003", "--ssl-certfile", "/certs/cert.pem", "--ssl-keyfile", "/certs/key.pem"]
