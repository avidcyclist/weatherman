import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('API_KEY')

lat = 40.4842  # Latitude for Bloomington
lon = -88.9937  # Longitude for Bloomington
url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely&units=metric&appid={api_key}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("API key is working correctly.")
    print(data)
else:
    print(f"Failed to fetch data: {response.status_code}")
    print(response.text)