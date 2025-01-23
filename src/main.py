import sqlite3
import os
import pandas as pd
import matplotlib.pyplot as plt

def connect_to_database(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection to database successful.")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def create_table(conn):
    """Create a table in the SQLite database."""
    try:
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS sample_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            UNIQUE(name, age)
        );
        """
        conn.execute(sql_create_table)
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def data_exists(conn, name, age):
    """Check if data already exists in the table."""
    try:
        sql_check_data = "SELECT 1 FROM sample_table WHERE name = ? AND age = ?"
        cursor = conn.cursor()
        cursor.execute(sql_check_data, (name, age))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Error checking data: {e}")
        return False

def insert_data(conn, data):
    """Insert data into the table."""
    try:
        sql_insert_data = "INSERT INTO sample_table (name, age) VALUES (?, ?)"
        for record in data:
            name, age = record
            if not data_exists(conn, name, age):
                conn.execute(sql_insert_data, (name, age))
        conn.commit()
        print("Data inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")

def query_data(conn):
    """Query and display data from the table."""
    try:
        df = pd.read_sql_query("SELECT * FROM sample_table", conn)
        print(df)
        return df
    except sqlite3.Error as e:
        print(f"Error querying data: {e}")
        return None

def visualize_data(df):
    """Visualize the data using matplotlib."""
    df.plot(kind='bar', x='name', y='age')
    plt.xlabel('Name')
    plt.ylabel('Age')
    plt.title('Age of Individuals')
    plt.show()

def main():
    # Use the correct relative path to the database file
    database = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_data.db')
    
    # Connect to the database
    conn = connect_to_database(database)
    
    if conn:
        # Create table
        create_table(conn)
        
        # Sample data to insert (replace this with your data fetching logic)
        new_data = [('Alice', 30), ('Bob', 25), ('Charlie', 35)]
        
        # Insert data
        insert_data(conn, new_data)
        
        # Query data
        df = query_data(conn)
        
        # Visualize data
        if df is not None:
            visualize_data(df)
        
        # Close the connection
        conn.close()

if __name__ == '__main__':
    main()