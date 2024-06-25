from db_connect import db_connect

import os
import sqlite3
import pickle

# Create folder if not exist
os.makedirs("src/schemas", exist_ok=True)

def extract_db_schema(db_path):
# def extract_db_schema(db_path, schema_file):
    """
    Extracts the schema of an SQLite database and saves it to a file using pickle.

    Parameters:
    db_path (str): Path to the SQLite database file.
    schema_file (str): Path to the file where the schema will be saved.
    """
    conn, db_name = db_connect(db_path)
    if conn is None:
        print(f"Connection to {db_name} database failed!")
        return  # Exit the function if connection to the database failed
    
    try:
        cursor = conn.cursor()
        print(f"Successfully connected to the {db_name} database. Fetching the schema definitions from {db_name} database...")

        # Query to get the database schema
        cursor.execute("SELECT sql FROM sqlite_master WHERE type IN ('table', 'index', 'view', 'trigger')")
        print(f"Successfully queried the {db_name} database. Extracting the schema...")

        # Fetch all schema definitions
        schema_definitions = [schema[0] for schema in cursor.fetchall()]
        print(f"Successfully extracted the schema from the {db_name} database. Saving the schema file...")

        output_directory = f"src/schemas/{db_name}_schema.pkl"

        # Save the schema definitions to a file using pickle
        with open(output_directory, "wb") as f:
        # with open(schema_file, "wb") as f:
            pickle.dump(schema_definitions, f)

        print(f"Successfully saved the schema file to the {output_directory}. Closing the {db_name} database connection.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        if conn:
            conn.close()

if __name__ == "__main__":
    db_path = "././data/northwind.db"
    extract_db_schema(db_path)