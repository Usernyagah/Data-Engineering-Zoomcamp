-- REPLACE THE FOLLOWING PLACEHOLDERS:
-- `your-project-id` -> Your GCP Project ID
-- `trips_data_all` -> Your BigQuery Dataset Name
-- `your-bucket-name` -> Your GCS Bucket Name

-- Create an external table using the Yellow Taxi Trip Records
CREATE OR REPLACE EXTERNAL TABLE `your-project-id.trips_data_all.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://your-bucket-name/yellow_tripdata_2024-*.parquet']
);

-- Create a (regular) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table)
CREATE OR REPLACE TABLE `your-project-id.trips_data_all.yellow_tripdata_non_partitioned` AS
SELECT * FROM `your-project-id.trips_data_all.external_yellow_tripdata`;

-- Question 5: Partitioning and clustering strategy
-- Create a new table partitioned by tpep_dropoff_datetime and clustered on VendorID
CREATE OR REPLACE TABLE `your-project-id.trips_data_all.yellow_tripdata_partitioned`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `your-project-id.trips_data_all.external_yellow_tripdata`;
