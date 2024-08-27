import requests
import json

# Define the API endpoint
url = "https://pubcasefinder.dbcls.jp/api/pcf_get_ranked_list"

# Define the query parameters
params = {
    'target': 'omim',  # or 'orphanet' or 'gene'
    'format': 'json',  # or 'tsv'
    'hpo_id': 'HP:0002089,HP:0001998'  # HPO IDs with commas
}

try:
    # Make the GET request with the parameters
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print("API Response:")
        #print(data)

        # Save the data to a JSON file
        with open('api_response.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print("Data has been saved to 'api_response.json'.")

    else:
        print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
