FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

WORKDIR /app/backend/

COPY pyproject.toml /app/
COPY poetry.lock /app/ 

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

RUN mkdir -p /app/backend/authentication/authentication && chmod -R 777 /app/backend/authentication/authentication

COPY . /app/backend

ENV PYTHONPATH=/app/backend

EXPOSE 8001

CMD ["uvicorn", "authentication.authentication_main:auth_app", "--host", "0.0.0.0", "--port", "8001" , "--ssl-certfile", "/certs/cert.pem", "--ssl-keyfile", "/certs/key.pem"]

