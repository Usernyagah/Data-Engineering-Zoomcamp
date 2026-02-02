
# Module 2: Workflow Orchestration Homework

This folder contains the solution and code for the Module 2 homework of the Data Engineering Zoomcamp.

## Quiz Answers

1.  **Yellow Taxi 2020-12 uncompressed size:** `128.3 MiB`
2.  **Rendered value of variable file:** `green_tripdata_2020-04.csv`
3.  **Yellow Taxi 2020 total rows:** `24,648,499`
4.  **Green Taxi 2020 total rows:** `1,734,051`
5.  **Yellow Taxi 2021-03 rows:** `1,925,152`
6.  **Schedule trigger timezone config:** `Add a timezone property set to America/New_York in the Schedule trigger configuration`

## Kestra Flows (Assignment & Challenge)

This repository includes the Kestra flow configurations used to solve the assignment and challenge parts of the homework. You can find them in the `flows/` directory:

*   **`flows/08_gcp_taxi_etl.yaml`**: 
    *   Modified version of the standard ETL flow.
    *   **Assignment**: Updated `inputs.year` to allow "2021" as a custom value, enabling the processing of 2021 data.
*   **`flows/09_gcp_taxi_scheduled.yaml`**: 
    *   **Quiz Q6**: Updated the `Schedule` triggers to include `timezone: "America/New_York"`.
*   **`flows/10_gcp_taxi_backfill_2021.yaml`**: 
    *   **Challenge Solution**: A flow that backfills Yellow and Green taxi data for the months 2021-01 through 2021-07.
    *   Uses a `ForEach` task to loop through the months.
    *   Uses `Subflow` tasks to trigger the `08_gcp_taxi_etl` flow for each month and taxi type (Yellow/Green).

## Analysis Script (Quiz Data Verification)

The file `solution_analysis.py` contains the Python code used to programmatically verify the file sizes and row counts for the quiz questions, ensuring 100% accuracy without needing to fully ingest the data first.

### Usage

To run the analysis script (requires `curl`, `zcat`, and `wc` installed on the system):

```bash
python3 solution_analysis.py
```

### Script Logic

The script uses `concurrent.futures` to parallelize data fetching:
- It iterates through the months of 2020 for both Yellow and Green taxis to calculate total row counts.
- It fetches the March 2021 Yellow taxi file for the specific quiz question.
- It verifies the uncompressed size of the Yellow 2020-12 file.
