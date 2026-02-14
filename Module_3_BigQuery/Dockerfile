FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY load_yellow_taxi_data.py .

# Entry point is the ingestion script
ENTRYPOINT [ "python", "load_yellow_taxi_data.py" ]
