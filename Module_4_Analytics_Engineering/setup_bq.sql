-- Create External Tables for Yellow and Green Taxi Data (2019-2020)
-- Create External Table for FHV Taxi Data (2019)

-- REPLACE THE FOLLOWING PLACEHOLDERS:
-- `your-project-id` -> Your GCP Project ID
-- `nytaxi` -> Your BigQuery Dataset Name
-- `your-bucket-name` -> Your GCS Bucket Name

-- Green Taxi External Table
CREATE OR REPLACE EXTERNAL TABLE `your-project-id.nytaxi.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://your-bucket-name/green/green_tripdata_20*.parquet']
);

-- Yellow Taxi External Table
CREATE OR REPLACE EXTERNAL TABLE `your-project-id.nytaxi.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://your-bucket-name/yellow/yellow_tripdata_20*.parquet']
);

-- FHV Taxi External Table
CREATE OR REPLACE EXTERNAL TABLE `your-project-id.nytaxi.external_fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://your-bucket-name/fhv/fhv_tripdata_2019-*.parquet']
);

-- Create Regular Tables (Materialized)
CREATE OR REPLACE TABLE `your-project-id.nytaxi.green_tripdata` AS
SELECT * FROM `your-project-id.nytaxi.external_green_tripdata`;

CREATE OR REPLACE TABLE `your-project-id.nytaxi.yellow_tripdata` AS
SELECT * FROM `your-project-id.nytaxi.external_yellow_tripdata`;

CREATE OR REPLACE TABLE `your-project-id.nytaxi.fhv_tripdata` AS
SELECT * FROM `your-project-id.nytaxi.external_fhv_tripdata`;
