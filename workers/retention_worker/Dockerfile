FROM python:3.12-slim

WORKDIR /app
COPY . /app

CMD ["python", "-m", "workers.retention_worker.main", "--help"]
