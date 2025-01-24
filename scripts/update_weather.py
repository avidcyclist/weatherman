import requests
import sqlite3
from dotenv import load_dotenv
import os
from datetime import datetime
import pytz

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('API_KEY')

# List of cities with their latitude and longitude
cities = [
    {'name': 'Bloomington', 'lat': 40.4842, 'lon': -88.9937, 'timezone': 'America/Chicago'},
    {'name': 'Marquette', 'lat': 46.5476, 'lon': -87.3956, 'timezone': 'America/Detroit'},
    {'name': 'Baraboo', 'lat': 43.4719, 'lon': -89.7446, 'timezone': 'America/Chicago'},
    {'name': 'Zurich', 'lat': 47.3769, 'lon': 8.5417, 'timezone': 'Europe/Zurich'},
    {'name': 'Norilsk', 'lat': 69.3558, 'lon': 88.1893, 'timezone': 'Asia/Krasnoyarsk'},
    {'name': 'Nashville', 'lat': 36.1627, 'lon': -86.7816, 'timezone': 'America/Chicago'}
]

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

# Create a new table for weather summary if it doesn't exist
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

# Function to generate a detailed summary
def generate_summary(weather_description, temperature_c, temperature_f, feels_like_c, feels_like_f, wind_speed, humidity, temp_min_c, temp_max_c, temp_min_f, temp_max_f):
    return (f"The forecast for today is {weather_description}. "
            f"The temperature is {temperature_c}°C ({temperature_f}°F), "
            f"feels like {feels_like_c}°C ({feels_like_f}°F). "
            f"Wind speed is {wind_speed} m/s with a humidity of {humidity}%. "
            f"The minimum temperature is {temp_min_c}°C ({temp_min_f}°F) and the maximum temperature is {temp_max_c}°C ({temp_max_f}°F).")


for city in cities:
    city_name = city['name']
    city_timezone = city['timezone']
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={city["lat"]}&lon={city["lon"]}&exclude=minutely&units=metric&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        current_weather = data['current']
        daily_weather = data['daily'][0]
        weather_description = current_weather['weather'][0]['description']
        temperature_c = current_weather['temp']
        temperature_f = round((temperature_c * 9/5) + 32, 2)
        feels_like_c = current_weather['feels_like']
        feels_like_f = round((feels_like_c * 9/5) + 32, 2)
        wind_speed = current_weather['wind_speed']
        humidity = current_weather['humidity']
        temp_min_c = daily_weather['temp']['min']
        temp_max_c = daily_weather['temp']['max']
        temp_min_f = round((temp_min_c * 9/5) + 32, 2)
        temp_max_f = round((temp_max_c * 9/5) + 32, 2)
        summary = generate_summary(weather_description, temperature_c, temperature_f, feels_like_c, feels_like_f, 
                                   wind_speed, humidity, temp_min_c, temp_max_c, temp_min_f, temp_max_f)

        # Convert UTC timestamp to local time
        utc_timestamp = datetime.utcfromtimestamp(current_weather['dt'])
        local_timezone = pytz.timezone(city_timezone)
        local_timestamp = utc_timestamp.replace(tzinfo=pytz.utc).astimezone(local_timezone)

        # Insert data into table
        cursor.execute('''
            INSERT INTO weather (city, weather, temperature, temperature_f, feels_like, feels_like_f, wind_speed, humidity, timestamp, timestamp_local)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (city_name, weather_description, temperature_c, temperature_f, feels_like_c, feels_like_f, wind_speed, humidity, utc_timestamp, local_timestamp))

        # Get the last inserted id from the weather table
        weather_id = cursor.lastrowid
        # Insert data into the weather_summary table
        cursor.execute('''
            INSERT INTO weather_temperatures (weather_id, city, temperature, temperature_f, feels_like, feels_like_f, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (weather_id, city_name, temperature_c, temperature_f, feels_like_c, feels_like_f, utc_timestamp))
        
        cursor.execute('''
            INSERT INTO weather_summary (weather_id, city, summary, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (weather_id, city_name, summary, utc_timestamp))

        print(f"Data for {city_name} inserted successfully.")
    else:
        print(f"Failed to fetch data for {city_name}: {response.status_code}")

# Commit and close connection
conn.commit()
conn.close()