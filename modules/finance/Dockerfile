FROM python:3.12-slim
WORKDIR /app
COPY modules/shared /app/shared
COPY modules/finance/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY modules/finance /app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
