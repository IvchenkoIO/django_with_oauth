FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
ENV FORCE_SCRIPT_NAME=/resource
ENV DJANGO_SETTINGS_MODULE=resource_server.settings

WORKDIR /app

# PostgreSQL
RUN apt-get update && apt-get install -y libpq-dev gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8001

CMD ["sh", "-c", "\
    python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn resource_server.wsgi:application --bind 0.0.0.0:8001 \
"]
