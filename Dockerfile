# Use a slim Python image for efficiency
FROM python:3.11-slim

# Set environment variables for the application
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE core.settings

# Set the working directory inside the container
WORKDIR /usr/src/app

# Install system dependencies needed for psycopg2 (PostgreSQL adapter)
# We use 'libpq-dev' to allow Python's psycopg2 to compile
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Django default port
EXPOSE 8000