from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
import os
from dotenv import load_dotenv
from datetime import datetime
import pytz
import logging
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Weather API key
API_KEY = os.getenv('API_KEY')

# Bloomington city details
city = {
    'name': 'Bloomington',
    'lat': 40.4842,
    'lon': -88.9937,
    'timezone': 'America/Chicago'
}

def get_weather_data(city):
    try:
        # Fetch weather data from external API
        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={city["lat"]}&lon={city["lon"]}&exclude=minutely&units=metric&appid={API_KEY}'
        logging.debug(f"Fetching weather data from URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        logging.debug(f"Weather data received: {weather_data}")

        current_weather = weather_data['current']
        daily_weather = weather_data['daily'][0]
        weather_desc = current_weather['weather'][0]['description']
        temp_c = current_weather['temp']
        temp_f = round((temp_c * 9/5) + 32, 1)
        feels_like_c = current_weather['feels_like']
        feels_like_f = round((feels_like_c * 9/5) + 32, 1)
        wind_speed_mps = current_weather['wind_speed']
        wind_speed_mph = round(wind_speed_mps * 2.23694, 1)
        humidity = current_weather['humidity']
        temp_min_c = daily_weather['temp']['min']
        temp_max_c = daily_weather['temp']['max']
        temp_min_f = round((temp_min_c * 9/5) + 32, 2)
        temp_max_f = round((temp_max_c * 9/5) + 32, 2)

        # Convert UTC timestamp to local time
        utc_timestamp = datetime.utcfromtimestamp(current_weather['dt'])
        local_timezone = pytz.timezone(city['timezone'])
        local_timestamp = utc_timestamp.replace(tzinfo=pytz.utc).astimezone(local_timezone)

        weather = (city['name'], weather_desc, temp_c, temp_f, feels_like_c, feels_like_f, wind_speed_mph, humidity, utc_timestamp, local_timestamp)
        logging.debug(f"Weather data fetched for {city['name']}: {weather}")
        return weather
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}", exc_info=True)
        return None

@app.route('/voice', methods=['POST'])
def voice():
    try:
        logging.debug("Received a call request")
        weather = get_weather_data(city)
        if weather:
            city_name, weather_desc, temp_c, temp_f, feels_like_c, feels_like_f, wind_speed_mph, humidity, timestamp, timestamp_local = weather
            local_time = datetime.now(pytz.timezone('America/Chicago')).strftime('%I:%M %p')
            response_text = (f"Hello, the current time in Bloomington is {local_time}. "
                             f"The current weather in {city_name} is {weather_desc}. "
                             f"The temperature is {temp_f} degrees Fahrenheit, "
                             f"feels like {feels_like_f} degrees. "
                             f"Wind speed is {wind_speed_mph} miles per hour with a humidity of {humidity} percent. "
                             f"Goodbye. ")
        else:
            response_text = "Sorry, I couldn't retrieve the weather data at this time."

        response = VoiceResponse()
        response.say(response_text)
        logging.debug(f"Response text: {response_text}")
        response.pause(length=5)  # Add a 5-second pause at the end
        return Response(str(response), mimetype='text/xml')
    except Exception as e:
        logging.error(f"Error in /voice endpoint: {e}", exc_info=True)
        return Response("Internal Server Error", status=500)
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)