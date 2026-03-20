import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
conn.autocommit = True
cursor = conn.cursor()

# Table for Question 4
cursor.execute("""
    CREATE TABLE IF NOT EXISTS trips_per_pulocation_5min (
        window_start TIMESTAMP,
        PULocationID INT,
        num_trips INT
    );
""")

# Table for Question 5
cursor.execute("""
    CREATE TABLE IF NOT EXISTS longest_session_pulocation (
        window_start TIMESTAMP,
        window_end TIMESTAMP,
        PULocationID INT,
        num_trips INT
    );
""")

# Table for Question 6
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tip_amount_1hr (
        window_start TIMESTAMP,
        total_tip_amount FLOAT
    );
""")

# Clean previous data if any
cursor.execute("TRUNCATE TABLE trips_per_pulocation_5min;")
cursor.execute("TRUNCATE TABLE longest_session_pulocation;")
cursor.execute("TRUNCATE TABLE tip_amount_1hr;")

print("Tables created successfully!")
cursor.close()
conn.close()
