import sqlite3
import os

# Connect to SQLite database (or create it if it doesn't exist)
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'weather_data.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign key support
cursor.execute('PRAGMA foreign_keys = ON')

# Function to add column if it doesn't exist
def add_column_if_not_exists(cursor, table_name, column_name, column_type):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [info[1] for info in cursor.fetchall()]
    if column_name not in columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")

# Example of how to add a new column if it doesn't exist
# Uncomment and modify the following line to add a new column - cursor, table name, new column, new column data type
# add_column_if_not_exists(cursor, 'weather', 'new_column_name', 'new_column_data_type')
# Create table with correct schema if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY,
        city TEXT,
        weather TEXT,
        temperature REAL,
        temperature_f REAL,
        feels_like REAL,
        feels_like_f REAL,
        wind_speed REAL,
        humidity REAL,
        timestamp DATETIME,
        timestamp_local DATETIME
    )
''')

# Create a new table for weather temperatures if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_temperatures (
        id INTEGER PRIMARY KEY,
        weather_id INTEGER,
        city TEXT,
        temperature REAL,
        temperature_f REAL,
        feels_like REAL,
        feels_like_f REAL,
        timestamp DATETIME,
        FOREIGN KEY (weather_id) REFERENCES weather(id)
    )
''')

# Create a new table for weather summary if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_summary (
        id INTEGER PRIMARY KEY,
        weather_id INTEGER,
        city TEXT,
        summary TEXT,
        timestamp DATETIME,
        FOREIGN KEY (weather_id) REFERENCES weather(id)
    )
''')

# Commit and close connection
conn.commit()
conn.close()

print("Tables created successfully.")