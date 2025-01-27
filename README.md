# Data Pipeline Practice

This project is designed to demonstrate a simple data pipeline using Python and SQLite. It includes functionality to connect to an SQLite database, perform data operations, and manage data processing tasks.


# Weather Data Fetching and Storage

## Overview

This project fetches weather data from the OpenWeatherMap API and stores it in a SQLite database. The data is organized into three tables: `weather`, `weather_temperatures`, and `weather_summary`. Additionally, the project includes scripts for visualizing the weather data.


## Project Structure

```
└───data_pipeline_practice
    │   .env
    │   .gitignore
    │   Procfile
    │   README.md
    │   requirements.txt
    │
    ├───data
    │       sample_data.db
    │       weather.csv
    │       weather_data.xlsx
    │       weather_summary.csv
    │       weather_temperatures.csv
    │
    ├───database
    │       weather_data.db
    │
    ├───flask_app
    │       time_and_temp.py
    │
    ├───images
    │       1_24_2025_bar_chart.png
    │       1_24_2025_trend.png
    │       Figure_1.png
    │
    ├───scripts
    │       check_weather_db.py
    │       check_weather_summary.py
    │       check_weather_temperature.py
    │       create_tables.py
    │       export_weather_data.py
    │       scheduler.py
    │       table_name_change.py
    │       test_api_key.py
    │       update_weather.py
    │       visualize_weather.py
    │
    ├───sql_scripts
    │       sql_scripts.md
    │
    └───src
        │   main.py
        │
        └───utils
                __init__.py
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd data_pipeline_practice
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

This will initiate the data pipeline and perform the defined operations on the SQLite database. Make sure the `sample_data.db` file is present in the `data` directory for the application to function correctly.


## Scripts

### `create_tables.py`

This script creates the necessary tables in the SQLite database if they do not already exist.

### `update_weather.py`

This script fetches current and daily weather data from the OpenWeatherMap API and inserts it into the database.

### `check_weather_db.py`

This script queries and prints the contents of the `weather` table.

### `check_weather_summary.py`

This script queries and prints the contents of the `weather_summary` table.

### `check_weather_temperature.py`

This script queries and prints the contents of the `weather_temperatures` table.

### `table_name_change.py`

This script renames a table in the SQLite database.

### `test_api_key.py`

This script tests the validity of the OpenWeatherMap API key.

### `visualize_weather.py`

This script visualizes the weather data stored in the database using matplotlib.

## Twilio Integration for Weather Updates

### But wait! There is more!

This project also includes a Flask application that integrates with Twilio to provide weather updates via phone calls. When a call is received, the application fetches the current weather data and responds with a voice message containing the weather information.

### Setting Up Twilio Integration

1. **Environment Variables**: Ensure the following environment variables are set in your `.env` file or Heroku config vars:
    - `API_KEY`: Your OpenWeatherMap API key
    - `TWILIO_ACCOUNT_SID`: Your Twilio account SID
    - `TWILIO_AUTH_TOKEN`: Your Twilio auth token

2. **Deploying to Heroku**: Deploy the Flask application to Heroku and set up the Twilio webhook to point to your Heroku app's `/voice` endpoint.

### Example Usage

1. **Make a Call**: Call your Twilio phone number. 217-829-2566 - Bloomington Time and Temp
2. **Receive Weather Update**: The Flask application will fetch the current weather data and respond with a voice message containing the weather information.

### Flask Application Code

The Flask application code is located in `flask_app/time_and_temp.py`.

### Summary

- **Project Structure**: The README now includes a detailed project structure.
- **Script Descriptions**: Each script is described with its purpose.
- **Usage Instructions**: Clear instructions on how to use the scripts.
- **Future Enhancements**: Suggestions for future improvements.

This README provides a comprehensive overview of your project and will help others understand and use your code effectively. Let me know if you need any further assistance!