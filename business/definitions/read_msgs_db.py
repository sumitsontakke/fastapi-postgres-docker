import sys
import os
from imessage_reader import fetch_data

DB_PATH = os.getenv("DATA_DIRECTORY", "/Users/sumitsontakke/Documents/")


# Create a FetchData instance
fd = fetch_data.FetchData(DB_PATH + "chat.db")

# Store messages in my_data
# This is a list of tuples containing user id, message and service (iMessage or SMS).
my_data = fd.get_messages()
