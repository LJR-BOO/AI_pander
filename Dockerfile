# Simple Dockerfile for running the Streamlit app
FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable buffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Streamlit recommended envs for server
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_ENABLE_WEBRTC=false
ENV PORT=8501

WORKDIR /app

# system deps (if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for Docker layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project
COPY . /app

EXPOSE 8501

# Use .env file in docker-compose or pass envs via CLI
CMD ["streamlit", "run", "ai_companion_app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
