import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# File paths
input_file = 'unique_ids.txt'
output_file = 'xp_list.txt'
temp_file = 'temp_xp_list.txt'  # Temporary file to store results before deduplication

# Base URL for requests
base_url = 'https://kirka.irrvlo.xyz/_next/data/Qj7Evkvz7SgKQYk1Q4HmZ/users/'

def fetch_user_data(user_id):
    # Strip the '#' from the beginning of the user ID
    clean_user_id = user_id[1:] if user_id.startswith('#') else user_id

    # Construct the full URL
    url = f'{base_url}{clean_user_id}.json'

    try:
        # Make the GET request
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Parse the JSON response
        data = response.json()

        # Extract the required data
        level = data['pageProps']['userData']['level']
        xp_until_next_level = data['pageProps']['userData']['xpUntilNextLevel']

        # Calculate the next level
        next_level = level + 1

        # Return the result in the desired format
        return f"{next_level},{xp_until_next_level}"
    except Exception as e:
        # Print an error message and continue
        print(f"Request failed for user {user_id}: {e}")
        return None  # Return None if the request or parsing failed

def remove_duplicates(file_path):
    seen = set()
    with open(file_path, 'r') as in_file, open(output_file, 'w') as out_file:
        for line in in_file:
            if line not in seen:
                out_file.write(line)
                seen.add(line)

def main():
    # Read the user IDs from the input file
    with open(input_file, 'r') as in_file:
        user_ids = [line.strip() for line in in_file]

    # Use ThreadPoolExecutor to process requests concurrently
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(fetch_user_data, user_id): user_id for user_id in user_ids}

        with open(temp_file, 'w') as out_file:
            for future in as_completed(futures):
                result = future.result()
                if result:
                    out_file.write(result + '\n')
                    out_file.flush()
                    print(result)

    # Remove duplicates from the temporary file and save to the final output file
    remove_duplicates(temp_file)

    print(f"Data extraction completed. Results saved to {output_file}.")

if __name__ == "__main__":
    main()
