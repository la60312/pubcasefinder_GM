import re
import os
import argparse
import pandas as pd
import requests
import json
import base64

from pathlib import Path

# Define the API endpoint
URL = "https://pubcasefinder.dbcls.jp/api/pcf_get_ranked_list"


def analyze_image(input_file, output_dir, api_endpoint):
    file_predix = Path(input_file).stem
    with open(input_file, "rb") as f:
        img_raw_original = f.read()

    encode_image = base64.b64encode(img_raw_original)
    encode_image_str = encode_image.decode("utf-8")

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {"img": encode_image_str}

    auth = requests.auth.HTTPBasicAuth('your_username', 'your_password')
    r = requests.post(url=api_endpoint, json=PARAMS, auth=auth)
    # extracting data in json format
    status = r.status_code
    data = r.json()
    if status != 200:
        print(data)
    else:
        output_data = {}
        output_data['case_id'] = file_predix
        for key, value in data.items():
            output_data[key] = value
        output_filename = os.path.join(output_dir, "{}.json".format(file_predix))
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

    return data

def get_ranked_list(hpo_str):
    # Define the query parameters
    print(hpo_str)
    params = {
        'target': 'omim',
        'format': 'json',
        'hpo_id': hpo_str  # HPO IDs with commas
    }

    try:
        # Make the GET request with the parameters
        response = requests.get(URL, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
        else:
            print(f"Failed to retrieve data. HTTP Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return data


def get_rank(ranked_list, target_omim):
    count = 1
    for diagnosis in ranked_list:
        suggested_omim = diagnosis['id'].replace('OMIM:', '')
        if suggested_omim == str(target_omim):
            break
        count += 1

    return count


def get_gm_rank(ranked_list, target_omim):
    count = 1
    for diagnosis in ranked_list:
        suggested_omim = diagnosis['omim_id']
        if suggested_omim == target_omim:
            break
        count += 1

    return count


def save_to_json(data, filename):
    # Save the data to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print("Data has been saved to {}.".format(filename))


def analyze_case_hpo(hpo_str, output_filename):
    data = get_ranked_list(hpo_str)
    save_to_json(data, output_filename)
    return data


def parse_hpo(input_str):
    # Regular expression to find 'HP:' followed by exactly 7 digits
    pattern = r'HP:\d{7}'

    # Find all matches in the input string
    matches = re.findall(pattern, input_str)

    return matches


def load_cached_file(cached_dir, name):
    file_path = os.path.join(cached_dir, name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = None

    return data


def preprocess_metadata(filename):
    """Load metadata from a TSV file using pandas."""
    # Read the TSV file into a pandas DataFrame
    df = pd.read_csv(filename, delimiter='\t')
    input_images = []
    for _, row in df.iterrows():
        if pd.isna(row['HPO']):
            continue
        else:
            hpos = parse_hpo(row['HPO'])
            hpo_str = ','.join(hpos)
        image_data = {'image_name': row['image_name'],
                      'hpo': hpo_str,
                      'omim': int(row['omim']),
                      'disorder': row['disorder']
                      }
        input_images.append(image_data)

    return input_images

def main():
    parser = argparse.ArgumentParser(description="Request data from the PubCaseFinder API.")
    parser.add_argument('-m', '--metadata', type=str, help="The filename of the input metadata TSV file")
    parser.add_argument('--images_dir', type=str, help="Image input directory")
    parser.add_argument('--hpo_output_dir', type=str, help="Output directory")
    parser.add_argument('--gm_output_dir', type=str, help="Output directory")
    parser.add_argument('--hpo_cache_dir', type=str,
                        required=False, help="Use previous hpo cached data in cached directory")
    parser.add_argument('--gm_cache_dir', type=str,
                        required=False, help="Use previous GestaltMatcher cached data in cached directory")
    parser.add_argument('--gm_url', default='localhost', dest='gm_url',
                        help='URL to the api.')
    parser.add_argument('--gm_port', default=5000, dest='gm_port',
                        help='Port to the api.')

    args = parser.parse_args()

    gm_predict_URL = "http://{}:{}/predict".format(args.gm_url, args.gm_port)

    hpo_cache_dir = args.hpo_cache_dir
    if hpo_cache_dir:
        print('Use HPO cached data from cached directory.')
    hpo_output_dir = args.hpo_output_dir
    if not os.path.exists(hpo_output_dir):
        os.makedirs(hpo_output_dir)

    gm_cache_dir = args.gm_cache_dir
    if gm_cache_dir:
        print('Use GestaltMatcher cached data from cached directory.')
    gm_output_dir = args.gm_output_dir
    if not os.path.exists(gm_output_dir):
        os.makedirs(gm_output_dir)

    # Load the metadata from the TSV file
    input_images = preprocess_metadata(args.metadata)
    print(len(input_images))

    output_data = []
    for image_data in input_images:
        file_name = image_data['image_name'].split('.')[0] + '.json'
        output_filename = os.path.join(hpo_output_dir, file_name)
        if args.hpo_cache_dir:
            hpo_data = load_cached_file(hpo_cache_dir, file_name)
        else:
            hpo_data = analyze_case_hpo(image_data['hpo'], output_filename)

        if args.gm_cache_dir:
            gm_data = load_cached_file(gm_cache_dir, file_name)
        else:
            input_file = image_data['image_name']
            input_file = os.path.join(args.images_dir, input_file)
            if os.path.exists(input_file):
                gm_data = analyze_image(input_file, gm_output_dir, gm_predict_URL)

        image_data['hpo_rank'] = get_rank(hpo_data, image_data['omim'])
        if gm_data:
            image_data['gm_rank'] = get_gm_rank(gm_data['suggested_syndromes_list'], image_data['omim'])
        else:
            image_data['gm_rank'] = 0
        output_data.append(image_data)

    output_df = pd.DataFrame(output_data)
    output_df = output_df[['image_name',
                           'hpo_rank',
                           'gm_rank',
                           'disorder',
                           'omim',
                           'hpo']]
    output_df.to_csv('results.tsv', index=False, sep='\t')


if __name__ == '__main__':
    main()
