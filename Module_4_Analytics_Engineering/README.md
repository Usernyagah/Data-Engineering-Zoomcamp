# Module 4 Homework: Analytics Engineering with dbt

This directory contains the solution for the Module 4 homework.

## Setup & Execution

### Prerequisites
- Docker and Docker Compose.
- BigQuery dataset `nytaxi` and `dbt_prod` created.
- Service account key with BigQuery Admin permissions.

### Steps
1.  **Configure Environment**:
    - Build the environment and populate `.env` (use `.env.template` from Module 3 as a guide).
    - Ensure your service account key is available.

2.  **Data Ingestion**:
    - Run the ingestion container to load 2019-2020 data for Green, Yellow, and FHV.
    - Execute `setup_bq.sql` to create BigQuery tables.

3.  **dbt Build**:
    - Run `dbt build --target prod` inside the container.

---

## Homework Answers

### Question 1. dbt Lineage and Execution
**If you run `dbt run --select int_trips_unioned`, what models will be built?**
- **Answer**: `int_trips_unioned only`
  *(Note: dbt only builds the selected model. To build dependencies, you'd use `+int_trips_unioned` or `int_trips_unioned+`)*.

### Question 2. dbt Tests
**What happens when you run `dbt test --select fct_trips`?**
- **Answer**: `dbt will fail the test, returning a non-zero exit code`
  *(Note: The `accepted_values` test will find the value '6' which is not in the allowed list [1, 2, 3, 4, 5])*.

### Question 3. Counting Records in fct_monthly_zone_revenue
**What is the count of records in the fct_monthly_zone_revenue model?**
- **Answer**: `12,998`

### Question 4. Best Performing Zone for Green Taxis (2020)
**Which zone had the highest revenue?**
- **Answer**: `East Harlem North`

### Question 5. Green Taxi Trip Counts (October 2019)
**What is the total number of trips (total_monthly_trips) for Green taxis in October 2019?**
- **Answer**: `384,624`

### Question 6. Build a Staging Model for FHV Data
**What is the count of records in stg_fhv_tripdata?**
- **Answer**: `43,244,693`
  *(Note: This counts records where `dispatching_base_num` is not null for FHV 2019 data)*.
