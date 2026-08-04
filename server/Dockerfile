# Simple Dockerfile for the device-flow server
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py /app/app.py

EXPOSE 5000
# Use gunicorn for production process management
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "2", "--timeout", "120"]
