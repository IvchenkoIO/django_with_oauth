FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . /app

# Expose the port (8000 in this example)
EXPOSE 8000

# Start Gunicorn for the Django app (adjust the WSGI path as needed)
CMD ["gunicorn", "auth_server_django.wsgi:application", "--bind", "0.0.0.0:8000"]
