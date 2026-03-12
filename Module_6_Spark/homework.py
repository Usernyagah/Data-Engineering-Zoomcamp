import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os

# Create Spark Session
# Note: Questions 5 asks for the Spark UI port, which is 4040 by default.
spark = SparkSession.builder \
    .master("local[*]") \
    .appName('homework') \
    .config("spark.ui.port", "4040") \
    .getOrCreate()

print(f"Question 1: Spark version is {spark.version}")

# Read Data
input_path = 'yellow_tripdata_2025-11.parquet'
df = spark.read.parquet(input_path)

# Question 2: Repartition and Save
output_path = 'output/yellow/2025/11/'
df.repartition(4).write.mode('overwrite').parquet(output_path)

# Calculate average file size (Logic)
files = [f for f in os.listdir(output_path) if f.endswith('.parquet')]
if files:
    total_size = sum(os.path.getsize(os.path.join(output_path, f)) for f in files)
    avg_size_mb = (total_size / len(files)) / (1024 * 1024)
    print(f"Question 2: Average parquet file size is {avg_size_mb:.2f} MB")
else:
    print("Question 2: No output files found to calculate average size.")

# Question 3: Count trips on 15th Nov
# Answer pre-calculated: 162,604
df_15 = df.filter(F.to_date(df.tpep_pickup_datetime) == '2025-11-15')
print(f"Question 3: Trips on Nov 15th: {df_15.count()}")

# Question 4: Longest trip in hours
# Answer pre-calculated: 90.65
df_duration = df.withColumn('duration_hours', 
    (F.unix_timestamp('tpep_dropoff_datetime') - F.unix_timestamp('tpep_pickup_datetime')) / 3600
)
max_duration = df_duration.select(F.max('duration_hours')).collect()[0][0]
print(f"Question 4: Longest trip in hours: {max_duration:.2f}")

# Question 5: Spark UI Port
print("Question 5: Spark UI port is 4040")

# Question 6: Least frequent pickup location zone
# Answer pre-calculated: Governor's Island/Ellis Island/Liberty Island (1 trip)
df_zones = spark.read.option("header", "true").csv('taxi_zone_lookup.csv')
df_joined = df.join(df_zones, df.PULocationID == df_zones.LocationID)
least_frequent = df_joined.groupBy('Zone').count().orderBy('count').limit(1).collect()
print(f"Question 6: Least frequent pickup zone: {least_frequent[0]['Zone']} ({least_frequent[0]['count']} trips)")

spark.stop()
