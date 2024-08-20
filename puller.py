import requests
import json
import re

# Function to extract ID from the username
def extract_id(username):
    match = re.search(r'#\w+', username)
    return match.group(0) if match else None

# Function to process the JSON data
def extract_ids_from_json(json_data):
    ids = set()
    for trade in json_data:
        offerer_id = extract_id(trade.get('offerer', ''))
        accepter_id = extract_id(trade.get('accepter', ''))
        if offerer_id:
            ids.add(offerer_id)
        if accepter_id:
            ids.add(accepter_id)
    return ids

# Function to append unique IDs to a file
def append_unique_ids_to_file(ids, file_path):
    # Read existing IDs from the file
    try:
        with open(file_path, 'r') as file:
            existing_ids = set(line.strip() for line in file)
    except FileNotFoundError:
        existing_ids = set()

    # Find new IDs that are not already in the file
    new_ids = ids - existing_ids

    # Append new unique IDs to the file
    with open(file_path, 'a') as file:
        for id in new_ids:
            file.write(id + '\n')

# List of files to download
files = [
    "20240429_025958.json",
    "20240430_025958.json",
    "20240501_025958.json",
    "20240502_025958.json",
    "20240503_025958.json",
    "20240504_025958.json",
    "20240505_025958.json",
    "20240506_025958.json",
    "20240507_025958.json",
    "20240508_025958.json",
    "20240509_025958.json",
    "20240510_025958.json",
    "20240511_025958.json"
]

# Base URL
base_url = "https://kirka.lukeskywalk.com/tradehistory/"

# Output file for unique IDs
output_file = 'unique_ids.txt'

# Process each file
for file_name in files:
    url = base_url + file_name
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        ids = extract_ids_from_json(data)
        append_unique_ids_to_file(ids, output_file)
        print(f"Processed {file_name} and appended unique IDs.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download or process {file_name}: {e}")

print(f"All files processed. Unique IDs have been appended to {output_file}.")
