import duckdb

# Connect to in-memory database
con = duckdb.connect()

# Create tables from files
con.execute("CREATE TABLE trips AS SELECT * FROM read_parquet('green_tripdata_2025-11.parquet')")
con.execute("CREATE TABLE zones AS SELECT * FROM read_csv('taxi_zone_lookup.csv')")

print("--- Question 3 ---")
# Question 3: Counting short trips
res3 = con.execute("""
    SELECT count(*) 
    FROM trips 
    WHERE lpep_pickup_datetime >= '2025-11-01' 
      AND lpep_pickup_datetime < '2025-12-01' 
      AND trip_distance <= 1.0
""").fetchone()
print(f"Number of trips <= 1 mile in Nov 2025: {res3[0]}")

print("\n--- Question 4 ---")
# Question 4: Longest trip for each day
res4 = con.execute("""
    SELECT CAST(lpep_pickup_datetime AS DATE) as pickup_day, MAX(trip_distance) as max_dist
    FROM trips 
    WHERE trip_distance < 100
    GROUP BY pickup_day
    ORDER BY max_dist DESC
    LIMIT 1
""").fetchone()
print(f"Day with longest trip: {res4[0]} (Distance: {res4[1]})")

print("\n--- Question 5 ---")
# Question 5: Biggest pickup zone
res5 = con.execute("""
    SELECT z.Zone, SUM(t.total_amount) as total
    FROM trips t
    JOIN zones z ON t.PULocationID = z.LocationID
    WHERE CAST(t.lpep_pickup_datetime AS DATE) = '2026-11-18' -- Wait, the question said Nov 18th 2025.
    GROUP BY z.Zone
    ORDER BY total DESC
    LIMIT 1
""").fetchdf()
# Re-checking the date in the question... it says November 18th 2025.
# Let me check if the data has 2025 or 2026. Parquet file name is green_tripdata_2025-11.
res5_2025 = con.execute("""
    SELECT z.Zone, SUM(t.total_amount) as total
    FROM trips t
    JOIN zones z ON t.PULocationID = z.LocationID
    WHERE CAST(t.lpep_pickup_datetime AS DATE) = '2025-11-18'
    GROUP BY z.Zone
    ORDER BY total DESC
    LIMIT 1
""").fetchone()
print(f"Biggest pickup zone on 2025-11-18: {res5_2025}")

print("\n--- Question 6 ---")
# Question 6: Largest tip
res6 = con.execute("""
    SELECT dz.Zone, MAX(t.tip_amount) as max_tip
    FROM trips t
    JOIN zones pz ON t.PULocationID = pz.LocationID
    JOIN zones dz ON t.DOLocationID = dz.LocationID
    WHERE pz.Zone = 'East Harlem North'
      AND t.lpep_pickup_datetime >= '2025-11-01'
      AND t.lpep_pickup_datetime < '2025-12-01'
    GROUP BY dz.Zone
    ORDER BY max_tip DESC
    LIMIT 1
""").fetchone()
print(f"Drop off zone with largest tip from East Harlem North: {res6}")
