FROM python:3.12-slim

WORKDIR /app

# Install git for dbt packages
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables placeholders
ENV GCP_PROJECT_ID=""
ENV GCP_GCS_BUCKET=""
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"

ENTRYPOINT [ "/bin/bash" ]
