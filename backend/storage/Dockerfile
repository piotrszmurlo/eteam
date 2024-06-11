FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim

WORKDIR /app/backend/

COPY pyproject.toml /app/
COPY poetry.lock /app/ 

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev

RUN mkdir -p /app/backend/storage/storage && chmod -R 777 /app/backend/storage/storage

COPY . /app/backend

ENV PYTHONPATH=/app/backend

EXPOSE 8002

CMD ["uvicorn", "storage.storage_main:storage_app", "--host", "0.0.0.0", "--port", "8002"]