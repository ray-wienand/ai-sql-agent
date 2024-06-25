import os
import sqlite3

def db_connect(db_path):
    """
    Check if the database exists at the given path. 
    If it does not exist, return None and no further functions will run.

    By default, SQLite will create a new db if it doesn't exist. 
    But because it returns None, a new db is not created.
    """
    if not os.path.exists(db_path):
        print(f"Database {db_path} does not exist.")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        db_name = os.path.splitext(os.path.basename(db_path))[0]  # Remove .db extension
        print(f"Connection established with {db_name} database...")
        return conn, db_name
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None, None

if __name__ == "__main__":
    """
    The eastwind.db does not exist. 
    It is only included to test error handling.
    """
    # db_path = "..//data/eastwind.db" 
    db_path = "./data/northwind.db"
    db_connect(db_path)