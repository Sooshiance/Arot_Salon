# Use Python 3.11 slim base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=backend.settings

# Install system dependencies
RUN apt-get update && apt-get install -y netcat && apt-get clean

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (excluding dev files via .dockerignore)
COPY . .

# Create volume for database (for SQLite)
VOLUME /app/backend/db

# Expose port 8000
EXPOSE 8000

# Default command (overridden in compose)
CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
