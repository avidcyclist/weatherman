import requests
import sqlite3
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('API_KEY')

# List of cities with their latitude and longitude
cities = [
    {'name': 'Bloomington', 'lat': 40.4842, 'lon': -88.9937},
    {'name': 'Marquette', 'lat': 46.5476, 'lon': -87.3956},
    {'name': 'Baraboo', 'lat': 43.4719, 'lon': -89.7446},
    {'name': 'Zurich', 'lat': 47.3769, 'lon': 8.5417},
    {'name': 'Norilsk', 'lat': 69.3558, 'lon': 88.1893}
]

# Connect to SQLite database (or create it if it doesn't exist)
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'weather_data.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY,
        city TEXT,
        weather TEXT,
        temperature REAL,
        temperature_f REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

for city in cities:
    city_name = city['name']
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={city["lat"]}&lon={city["lon"]}&exclude=minutely&units=metric&appid={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        current_weather = data['current']
        weather_description = current_weather['weather'][0]['description']
        temperature_c = current_weather['temp']
        temperature_f = round((temperature_c * 9/5) + 32, 2)

        # Insert data into table
        cursor.execute('''
            INSERT INTO weather (city, weather, temperature, temperature_f)
            VALUES (?, ?, ?, ?)
        ''', (city_name, weather_description, temperature_c, temperature_f))

        print(f"Data for {city_name} inserted successfully.")
    else:
        print(f"Failed to fetch data for {city_name}: {response.status_code}")

# Commit and close connection
conn.commit()
conn.close()