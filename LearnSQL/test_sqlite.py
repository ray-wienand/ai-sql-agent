# Reference video: https://www.youtube.com/watch?v=c8yHTlrs9EA&t=267s

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data/alpha.db')

# Create a cursor object
cur = conn.cursor()

# Create a table if it does not exist
conn.execute('''CREATE TABLE IF NOT EXISTS people
                (first_name TEXT, last_name TEXT)''')


# Test Data
names_list = [
    ("Roderick", "Watson"),
    ("Roger", "Hom"),
    ("PetrinHalonen", ""),
    ("Jussi", ""),
    ("James", "McCann")
]

# Insert data into database
# ?. ? are placeholders to prevent sql injection
cur.executemany('''
    INSERT INTO people (first_name, last_nae) VALUES (?, ?) 
                ''', names_list)
conn.commit()

# Close the connection
conn.close()

