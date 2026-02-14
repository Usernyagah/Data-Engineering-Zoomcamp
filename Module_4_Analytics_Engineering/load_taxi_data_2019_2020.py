import os
import requests
from google.cloud import storage
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ==============================================================================
# CONFIGURATION
# ==============================================================================
BUCKET_NAME = os.environ.get("GCP_GCS_BUCKET")
PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        logging.info(f"File {source_file_name} uploaded to gs://{bucket_name}/{destination_blob_name}.")
    except Exception as e:
        logging.error(f"Failed to upload {source_file_name} to GCS: {e}")
        raise

def download_and_upload():
    # Yellow and Green: 2019, 2020
    # FHV: 2019
    tasks = [
        ("yellow", [2019, 2020]),
        ("green", [2019, 2020]),
        ("fhv", [2019])
    ]
    
    for taxi_type, years in tasks:
        for year in years:
            for month in range(1, 13):
                url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month:02d}.parquet"
                file_name = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
                
                logging.info(f"--- Processing {file_name} ---")
                
                try:
                    response = requests.get(url, stream=True)
                    if response.status_code == 200:
                        with open(file_name, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=81920):
                                f.write(chunk)
                        
                        logging.info(f"Uploading to GCS bucket: {BUCKET_NAME}...")
                        upload_to_gcs(BUCKET_NAME, file_name, f"{taxi_type}/{file_name}")
                        
                        # Clean up local file
                        os.remove(file_name)
                        logging.info(f"Cleaned up local file {file_name}")
                    else:
                        logging.error(f"Failed to download {url}. Status code: {response.status_code}")
                except Exception as e:
                    logging.error(f"An error occurred for {file_name}: {e}")

if __name__ == "__main__":
    if not BUCKET_NAME or not PROJECT_ID:
        logging.error("ERROR: GCP_GCS_BUCKET and GCP_PROJECT_ID environment variables must be set.")
    else:
        logging.info(f"Starting ingestion to project: {PROJECT_ID}, bucket: {BUCKET_NAME}")
        download_and_upload()
        logging.info("Ingestion process completed.")
