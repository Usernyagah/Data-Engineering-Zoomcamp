# Module 1 Homework: Docker & SQL (ZoomCamp Official Patterns)

## Data Ingestion (Official Script)
The ingestion script uses the official ZoomCamp pattern: `pandas` iterator with `chunksize`, `sqlalchemy` for database connection, and `argparse` for parameters.

### 1. Build the Ingestion Image
```bash
docker build -t taxi_ingest:v001 .
```

### 2. Run the Ingestion
Ensure your Postgres database is running via `docker-compose up -d`. Note that the network name is typically `module-1-docker-terraform_default`.

**Green Taxi Trips:**
```bash
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
docker run -it \
  --network=module-1-docker-terraform_default \
  taxi_ingest:v001 \
  --user=postgres \
  --password=postgres \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table_name=green_taxi_data \
  --url=${URL}
```

**Taxi Zones:**
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
docker run -it \
  --network=module-1-docker-terraform_default \
  taxi_ingest:v001 \
  --user=postgres \
  --password=postgres \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table_name=zones \
  --url=${URL}
```

## Question Answers

### Question 1. Understanding Docker images
**Answer:** `25.3`

### Question 2. Understanding Docker networking and docker-compose
**Answer:** `pgdatabase:5432`

### Question 3. Counting short trips
**Answer:** `8,007`
```sql
SELECT count(*) FROM green_taxi_data 
WHERE lpep_pickup_datetime >= '2025-11-01' AND lpep_pickup_datetime < '2025-12-01' 
AND trip_distance <= 1.0;
```

### Question 4. Longest trip for each day
**Answer:** `2025-11-14`
```sql
SELECT CAST(lpep_pickup_datetime AS DATE) as day, MAX(trip_distance) as dist 
FROM green_taxi_data WHERE trip_distance < 100 
GROUP BY day ORDER BY dist DESC LIMIT 1;
```

### Question 5. Biggest pickup zone
**Answer:** `East Harlem North`
```sql
SELECT z."Zone", SUM(t.total_amount) as total 
FROM green_taxi_data t JOIN zones z ON t."PULocationID" = z."LocationID" 
WHERE CAST(t.lpep_pickup_datetime AS DATE) = '2025-11-18' 
GROUP BY z."Zone" ORDER BY total DESC LIMIT 1;
```

### Question 6. Largest tip
**Answer:** `Yorkville West`
```sql
SELECT dz."Zone", MAX(t.tip_amount) as max_tip 
FROM green_taxi_data t 
JOIN zones pz ON t."PULocationID" = pz."LocationID" 
JOIN zones dz ON t."DOLocationID" = dz."LocationID" 
WHERE pz."Zone" = 'East Harlem North' 
AND t.lpep_pickup_datetime >= '2025-11-01' AND t.lpep_pickup_datetime < '2025-12-01' 
GROUP BY dz."Zone" ORDER BY max_tip DESC LIMIT 1;
```

### Question 7. Terraform Workflow
**Answer:** `terraform init, terraform apply -auto-approve, terraform destroy`
