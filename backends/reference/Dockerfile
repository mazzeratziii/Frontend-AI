FROM python:3.12.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi==0.116.1 uvicorn==0.35.0
COPY app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]