import json
from kafka import KafkaConsumer

def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

consumer = KafkaConsumer(
    'green-trips',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=json_deserializer,
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    consumer_timeout_ms=5000 # Wait for 5 seconds of inactivity before stopping
)

count = 0
for message in consumer:
    row = message.value
    # Count how many trips have a trip_distance greater than 5.0 kilometers
    if row.get('trip_distance', 0) > 5.0:
        count += 1

print(f"Number of trips with trip_distance > 5.0: {count}")
