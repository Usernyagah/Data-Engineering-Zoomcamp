# Module 3 Homework: Data Warehousing & BigQuery

This directory contains the code and SQL queries for the Module 3 homework.

## Setup & Data Ingestion

### Prerequisites
- Docker and Docker Compose installed.
- A Google Cloud Project with a GCS bucket and a BigQuery dataset created.
- A Service Account key file with appropriate permissions.

### Steps
1.  **Configure Environment**:
    - Copy `.env.template` to `.env`:
      ```bash
      cp .env.template .env
      ```
    - Update `.env` with your `GCP_PROJECT_ID`, `GCP_GCS_BUCKET`, `GCP_DATASET_NAME`, and the path to your service account key.

2.  **Run Ingestion**:
    - Build and run the ingestion container:
      ```bash
      docker-compose up --build
      ```
    - This will download the Yellow Taxi Parquet files (Jan-Jun 2024) and upload them to your GCS bucket.

3.  **BigQuery Setup**:
    - Execute the queries in `setup_bq.sql` in the BigQuery console (after replacing placeholders) to create the necessary tables.

---

## Homework Answers

### Question 1. Counting records
**What is count of records for the 2024 Yellow Taxi Data?**
- **Query**: `SELECT count(*) FROM your-project-id.trips_data_all.yellow_tripdata_non_partitioned;`
- **Answer**: `20,332,093`

### Question 2. Data read estimation
**What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?**
- **Query**: `SELECT COUNT(DISTINCT(PULocationID)) FROM your-project-id.trips_data_all.external_yellow_tripdata;` vs `SELECT COUNT(DISTINCT(PULocationID)) FROM your-project-id.trips_data_all.yellow_tripdata_non_partitioned;`
- **Answer**: `0 MB for the External Table and 155.12 MB for the Materialized Table`
  *(Note: External tables on Parquet files in GCS often show 0MB in preview/estimation because they are not yet read, while BQ tables have metadata about the column size)*.

### Question 3. Understanding columnar storage
**Why are the estimated number of Bytes different?**
- **Answer**: `BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.`

### Question 4. Counting zero fare trips
**How many records have a fare_amount of 0?**
- **Query**: `SELECT count(*) FROM your-project-id.trips_data_all.yellow_tripdata_non_partitioned WHERE fare_amount = 0;`
- **Answer**: `8,333`

### Question 5. Partitioning and clustering
**What is the best strategy to make an optimized table in Big Query...**
- **Answer**: `Partition by tpep_dropoff_datetime and Cluster on VendorID`

### Question 6. Partition benefits
**What are these values?**
- **Answer**: `310.24 MB for non-partitioned table and 26.84 MB for the partitioned table`

### Question 7. External table storage
**Where is the data stored in the External Table you created?**
- **Answer**: `GCP Bucket`

### Question 8. Clustering best practices
**It is best practice in Big Query to always cluster your data:**
- **Answer**: `False` *(Clustering is beneficial for large tables and specific query patterns, but not always necessary for small tables or when it doesn't align with usage)*.

### Question 9. Understanding table scans
**How many bytes does it estimate will be read? Why?**
- **Answer**: `0 bytes`. BigQuery stores metadata for row counts in regular tables, so `SELECT COUNT(*)` does not require scanning any data rows.
