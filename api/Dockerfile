FROM python:3.13.2-alpine

WORKDIR /api

COPY requirements.txt .env ./
COPY src ./src

RUN pip install -r requirements.txt

CMD ["sh", "-c", "uvicorn src.main:api --host 0.0.0.0 --port ${PORT}"]