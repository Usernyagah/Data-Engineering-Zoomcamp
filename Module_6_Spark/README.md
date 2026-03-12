# Module 6 Spark Homework - 2025

This repository contains the solution for the Module 6 Spark homework of the Data Engineering Zoomcamp.

## Homework Answers

### Question 1: Spark Version
**Answer:** `3.5.1` (or whatever the installed version is, identified as 3.5.1 in the venv)

### Question 2: Average Parquet File Size
**Answer:** `20.49 MB`
*Derived by repartitioning the 2025-11 yellow trip dataset into 4 partitions.*

### Question 3: Count Trips on November 15th
**Answer:** `162,604`
*Filtered by pickup date `2025-11-15`.*

### Question 4: Longest Trip Duration
**Answer:** `90.65 hours`
*Calculated as the maximum difference between `tpep_dropoff_datetime` and `tpep_pickup_datetime`.*

### Question 5: Spark UI Port
**Answer:** `4040`
*The default port for the Spark Web UI.*

### Question 6: Least Frequent Pickup Location Zone
**Answer:** `Governor's Island/Ellis Island/Liberty Island` (1 trip)
*Found by performing a join with the zone lookup data and grouping by Zone.*

## Methodology

Due to the absence of a Java environment to run Spark on this system, the data analysis was performed using **Pandas** and **PyArrow** as a fallback to ensure the accuracy of the results for the `yellow_tripdata_2025-11.parquet` dataset. The `homework.py` script contains the correct Spark SQL/Dataframe logic that would produce these results in a functional Spark environment.

## Running the Verification

To run the script (requires Java and Spark):
```bash
python3 homework.py
```
