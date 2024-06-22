import sqlite3

# Connect to or create SQLite database
conn =  sqlite3.connect('data/members.db')
cur = conn.cursor()

# Load SQL script from file
# Uncomment if table does not exist
# with open("test.sql") as file:
#   sql_script = file.read()
  
# Execute script
# Uncomment if table does not exist
# cur.executescript(sql_script)

# Display data
# member_data = cur.execute("SELECT * FROM members ORDER BY ln")
# for row in member_data:
#   print(row)

# Alternative display data
cur.execute("SELECT * FROM members ORDER BY ln")
for member in cur:
  print(member)

# Close the database
cur.close()
conn.close()