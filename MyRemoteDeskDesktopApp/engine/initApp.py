# Import required libraries
# 'moni' for mainRecord function
# 'json' for handling JSON objects
# 'sys' for command-line arguments
import moni
import json
import sys

# Load JSON object from the first command-line argument
# sys.argv[1] is used to get the first argument passed from the command line
# json.loads is used to parse a JSON string and convert it into a Python object
json_object = json.loads(sys.argv[1])

# Extract values from the JSON object
# 'e_id' and 'o_id' are extracted from the JSON object
# They are assumed to be keys in the JSON object
e_id = json_object["e_id"]
o_id = json_object["o_id"]

# Call the 'mainRecord' function with 'e_id' and 'o_id' as parameters
# The 'mainRecord' function is assumed to be defined in the 'moni' module
# 'e_id' and 'o_id' are passed to the 'mainRecord' function which executes
# relevant operation based on these values
moni.mainRecord(e_id, o_id)
