import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Connect to SQLite database
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'weather_data.db')
conn = sqlite3.connect(db_path)

# Query the database
df = pd.read_sql_query('SELECT * FROM weather', conn)

# Close the connection
conn.close()

# Convert timestamp columns to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['timestamp_local'] = pd.to_datetime(df['timestamp_local'])

# Plot the data
plt.figure(figsize=(14, 8))
for city in df['city'].unique():
    city_data = df[df['city'] == city]
    plt.plot(city_data['timestamp'], city_data['temperature_f'], label=city)

plt.xlabel('Timestamp (UTC)')
plt.ylabel('Temperature (F)')
plt.title('Temperature Trends')
plt.legend()
plt.grid(True)
plt.show()

# Plot the count of different weather types
weather_counts = df['weather'].value_counts()

plt.figure(figsize=(14, 8))
weather_counts.plot(kind='bar')
plt.xlabel('Weather Type')
plt.ylabel('Count')
plt.title('Count of Different Weather Types')
plt.grid(True)
plt.show()