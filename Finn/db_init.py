import sqlite3
import json


# Create a table with columns for tag, query list, and response list
with open('/Users/james04nesbitt/PycharmProjects/pythonProject/Finn/intents.json', 'r') as file:
    data = json.load(file)['intents']  # Access 'intents' key in the JSON

# Connect to the SQLite database
conn = sqlite3.connect('finn.db')
cursor = conn.cursor()

# Create a table with columns for tag, query list, and response list if not already created
cursor.execute('DELETE FROM TagData')
cursor.execute('CREATE TABLE IF NOT EXISTS TagData(tag text, query_list text, response_list text)')

# Insert each tag along with its query and response lists as JSON strings
for tag, data_values in data.items():
    query_list_json = json.dumps(data_values['queries'])
    response_list_json = json.dumps(data_values['responses'])
    cursor.execute('INSERT INTO TagData VALUES (?, ?, ?)', (tag, query_list_json, response_list_json))

# Commit changes and close the connection
conn.commit()
conn.close()