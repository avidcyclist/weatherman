import sqlite3
import os

# Connect to SQLite database
db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'weather_data.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Rename the table
cursor.execute('ALTER TABLE weather_summary RENAME TO weather_temperatures')

# Commit and close connection
conn.commit()
conn.close()

print("Table renamed successfully.")