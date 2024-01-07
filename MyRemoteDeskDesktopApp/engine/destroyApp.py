# Start by importing necessary modules.
import sys
import json
import moni
import mysql.connector
from datetime import date

# Establish a connection to the MySQL database using the provided credentials.
connectiondb = mysql.connector.connect(
  host="host", user="user",
  password="password", database="database", port=3306
)

# Create a cursor object to perform SQL operations.
cursordb = connectiondb.cursor()

# Print the database connection object for debugging purposes.
print(connectiondb)

# Parse the JSON object from the command line argument.
json_object = json.loads(sys.argv[1])

# Extract the 'e_id' and 'o_id' from the parsed JSON object.
e_id = json_object["e_id"]
o_id = json_object["o_id"]

# Use the 'show_activity' function from the 'moni' module
# to iterate over each activity.
for w, t in moni.show_activity():
    # Get the current date.
    today = date.today()

    # Construct the SQL query to insert the activity details into the database.
    sql = ("INSERT INTO MonitoringDetails "
           "(md_title, md_total_time_seconds, md_date, e_id_id, o_id_id) "
           "VALUES (%s, %s, %s, %s, %s)")

    # Bind the activity details to the SQL query.
    val = (w, t, today, e_id, o_id)

    # Execute the SQL query.
    cursordb.execute(sql, val)

    # Commit the transaction to the database.
    connectiondb.commit()

    # Print the number of rows affected by the insert operation for debugging purposes.
    print(cursordb.rowcount, "record inserted.")