FROM python:3.12-slim

WORKDIR /app
COPY api.py .

RUN pip install --no-cache-dir fastapi uvicorn

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
