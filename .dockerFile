FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.server.auth:app", "--host", "0.0.0.0", "--port", "10000"]