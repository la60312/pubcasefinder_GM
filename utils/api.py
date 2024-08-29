import os
import time
import json
import base64
import requests

from pathlib import Path


def analyze_image(input_file, output_dir, api_endpoint, auth=None):

    file_predix = Path(input_file).stem
    with open(input_file, "rb") as f:
        img_raw_original = f.read()

    encode_image = base64.b64encode(img_raw_original)
    encode_image_str = encode_image.decode("utf-8")

    PARAMS = {"img": encode_image_str}

    r = requests.post(url=api_endpoint, json=PARAMS, auth=auth)
    status = r.status_code
    data = r.json()

    if status != 200:
        print(data)
    else:
        output_data = {'case_id': file_predix}
        output_data.update(data)
        output_filename = os.path.join(output_dir, f"{file_predix}.json")
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

    return data


def get_pcf_ranked_list(hpo_str, target='omim', format='json',
                        url="https://pubcasefinder.dbcls.jp/api/pcf_get_ranked_list",
                        retries=3, backoff_factor=2):
    params = {
        'target': target,
        'format': format,
        'hpo_id': hpo_str
    }

    attempt = 0
    data = None

    while attempt < retries:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            break  # Exit the loop if the request is successful
        except requests.exceptions.RequestException as e:
            attempt += 1
            print(f"Attempt {attempt} failed with error: {e}. Retrying in {backoff_factor} seconds...")
            time.sleep(backoff_factor)  # Wait before retrying

            # Increase the backoff factor for the next retry
            backoff_factor *= 2

    if data is None:
        print("All retry attempts failed.")

    return data
