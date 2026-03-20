import json
import time
import pandas as pd
from kafka import KafkaProducer

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=json_serializer
)

df = pd.read_parquet('src/job/green_tripdata_2025-10.parquet')
columns = [
    'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'PULocationID', 'DOLocationID',
    'passenger_count', 'trip_distance', 'tip_amount', 'total_amount'
]
df = df[columns]

# Flink JSON parser expects valid numbers
df = df.fillna(0)

# Convert datetimes to string
df['lpep_pickup_datetime'] = df['lpep_pickup_datetime'].astype(str)
df['lpep_dropoff_datetime'] = df['lpep_dropoff_datetime'].astype(str)

t0 = time.time()

records = df.to_dict(orient='records')
for row_dict in records:
    producer.send('green-trips', value=row_dict)

producer.flush()

t1 = time.time()
print(f'took {(t1 - t0):.2f} seconds')
