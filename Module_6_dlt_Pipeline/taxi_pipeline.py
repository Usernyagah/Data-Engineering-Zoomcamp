"""
NYC Taxi Trip Data Pipeline using dlt + DuckDB
Loads paginated JSON data from the NYC Taxi API into DuckDB.

API: https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api
- Paginated JSON, 1000 records per page
- Stop when an empty page is returned
"""

import dlt
from dlt.sources.rest_api import rest_api_source


def nyc_taxi_source():
    """REST API source for NYC Yellow Taxi data."""
    config = {
        "client": {
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/",
        },
        "resources": [
            {
                "name": "rides",
                "endpoint": {
                    "path": "data_engineering_zoomcamp_api",
                    "method": "GET",
                    "paginator": {
                        "type": "page_number",
                        "base_page": 1,
                        "page_param": "page",
                        "total_path": None,
                        "stop_after_empty_page": True,
                    },
                    "data_selector": "$",
                },
            }
        ],
    }
    return rest_api_source(config)


def run_pipeline():
    """Create and run the taxi pipeline."""
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="nyc_taxi",
    )

    print("Loading NYC Taxi data into DuckDB...")
    load_info = pipeline.run(nyc_taxi_source())
    print(load_info)
    print("\nPipeline completed successfully!")

    # Quick verification queries
    with pipeline.sql_client() as client:
        with client.execute_query("SELECT COUNT(*) as total_rows FROM rides") as cursor:
            row = cursor.fetchone()
            print(f"\nTotal rows loaded: {row[0]:,}")

        with client.execute_query(
            """
            SELECT 
                MIN(trip_pickup_date_time) as start_date,
                MAX(trip_pickup_date_time) as end_date
            FROM rides
            """
        ) as cursor:
            row = cursor.fetchone()
            print(f"Date range: {row[0]} → {row[1]}")


if __name__ == "__main__":
    run_pipeline()
