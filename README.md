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
    │   README.md
    │   requirements.txt
    │
    ├───data
    │       sample_data.db
    │
    ├───database
    │       weather_data.db
    │
    ├───images
    │       Figure_1.png
    │
    ├───scripts
    │       check_weather_db.py
    │       check_weather_summary.py
    │       check_weather_temperature.py
    │       create_tables.py
    │       table_name_change.py
    │       test_api_key.py
    │       update_weather.py
    │       visualize_weather.py
    │
    ├───sql_scripts
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

### Summary

- **Project Structure**: The README now includes a detailed project structure.
- **Script Descriptions**: Each script is described with its purpose.
- **Usage Instructions**: Clear instructions on how to use the scripts.
- **Future Enhancements**: Suggestions for future improvements.

This README provides a comprehensive overview of your project and will help others understand and use your code effectively. Let me know if you need any further assistance!