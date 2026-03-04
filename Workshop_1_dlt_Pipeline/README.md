# Module 6: dlt Pipeline - NYC Taxi Data

Building a dlt pipeline that loads NYC Yellow Taxi trip data into DuckDB.

## Setup

```bash
# Uses the existing .venv in the project root
# dlt[duckdb] is installed in the venv
pip install "dlt[duckdb]"
```

## Running the Pipeline

```bash
python taxi_pipeline.py
```

## Running the Analysis

```bash
python analyze_taxi_data.py
```

## Dataset

- **Source**: [NYC Taxi API](https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api)
- **Format**: Paginated JSON (1,000 records/page)
- **Total records loaded**: 10,000

## Homework Answers

| Question | Answer |
|----------|--------|
| Q1: Date range of dataset | **2009-06-01 to 2009-07-01** |
| Q2: Credit card trip proportion | **26.66%** |
| Q3: Total tips generated | **$6,063.41** |
