import sqlite3
import os

# Connect to SQLite database
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'weather_data.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query the database
cursor.execute('SELECT * FROM weather_temperatures')
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()