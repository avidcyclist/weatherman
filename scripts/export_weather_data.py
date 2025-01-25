import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
# Get the output directory from environment variable
output_dir = os.getenv('OUTPUT_DIR')
# Connect to SQLite database
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'weather_data.db')
conn = sqlite3.connect(db_path)

# Query the database
weather_df = pd.read_sql_query('SELECT * FROM weather', conn)
weather_temperatures_df = pd.read_sql_query('SELECT * FROM weather_temperatures', conn)
weather_summary_df = pd.read_sql_query('SELECT * FROM weather_summary', conn)

# Close the connection
conn.close()

# Define the output directory

os.makedirs(output_dir, exist_ok=True)

# Export to CSV
weather_df.to_csv(os.path.join(output_dir, 'weather.csv'), index=False)
weather_temperatures_df.to_csv(os.path.join(output_dir, 'weather_temperatures.csv'), index=False)
weather_summary_df.to_csv(os.path.join(output_dir, 'weather_summary.csv'), index=False)

# Export to Excel
with pd.ExcelWriter(os.path.join(output_dir, 'weather_data.xlsx')) as writer:
    weather_df.to_excel(writer, sheet_name='Weather', index=False)
    weather_temperatures_df.to_excel(writer, sheet_name='Weather Temperatures', index=False)
    weather_summary_df.to_excel(writer, sheet_name='Weather Summary', index=False)

print("Data exported successfully.")