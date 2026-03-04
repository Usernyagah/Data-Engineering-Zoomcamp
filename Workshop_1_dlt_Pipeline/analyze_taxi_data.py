"""
NYC Taxi Data Analysis Queries
Answers the homework questions using the loaded DuckDB data.
"""

import dlt


def analyze():
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="nyc_taxi",
    )

    with pipeline.sql_client() as client:
        print("=" * 50)
        print("NYC Taxi Data Analysis - Homework Answers")
        print("=" * 50)

        # Q1: Date range
        print("\nQ1: Dataset Date Range")
        with client.execute_query(
            """
            SELECT 
                MIN(trip_pickup_date_time) as start_date, 
                MAX(trip_pickup_date_time) as end_date,
                COUNT(*) as total_trips
            FROM rides
            """
        ) as cursor:
            row = cursor.fetchone()
            print(f"  Start date : {str(row[0])[:10]}")
            print(f"  End date   : {str(row[1])[:10]}")
            print(f"  Total trips: {row[2]:,}")

        # Q2: Payment type proportions
        print("\nQ2: Payment Type Distribution")
        with client.execute_query(
            """
            SELECT 
                payment_type, 
                COUNT(*) as count, 
                ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as pct
            FROM rides 
            GROUP BY payment_type 
            ORDER BY count DESC
            """
        ) as cursor:
            for row in cursor.fetchall():
                print(f"  {row[0]}: {row[1]:,} trips ({row[2]}%)")

        # Q3: Total tips
        print("\nQ3: Total Tips Generated")
        with client.execute_query(
            "SELECT ROUND(SUM(tip_amt), 2) as total_tips FROM rides"
        ) as cursor:
            row = cursor.fetchone()
            print(f"  Total tips: ${row[0]:,.2f}")

        print("\n" + "=" * 50)
        print("Answers:")
        print("  Q1: 2009-06-01 to 2009-06-30")
        print("  Q2: Credit card = 26.66%")
        print("  Q3: Total tips = $6,063.41")


if __name__ == "__main__":
    analyze()
