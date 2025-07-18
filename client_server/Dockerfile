# client_server/Dockerfile

# Use a slim Python image for a small footprint
FROM python:3.9-slim

# Disable Python buffering (so logs show up immediately)
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the image
COPY . /app

# Expose the port the app will run on
EXPOSE 8002

# Run the Django app via Gunicorn (its better to use tools like gunicorn for prod, otherwise may result in a bad concurrent performance)
CMD ["gunicorn", "client_service.wsgi:application", "--bind", "0.0.0.0:8002"]
