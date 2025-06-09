# client_server/Dockerfile
FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8002
CMD ["gunicorn", "client_service.wsgi:application", "--bind", "0.0.0.0:8002"]
