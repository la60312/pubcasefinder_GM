import os
import json
import pandas as pd
from utils.hpo import parse_hpo


def preprocess_jstage_metadata(filename):
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
                      'disorder': row['disorder']}
        input_images.append(image_data)

    return input_images


def preprocess_gmdb_metadata(filename):
    df = pd.read_csv(filename, delimiter='\t')
    input_images = []
    for _, row in df.iterrows():
        if pd.isna(row['present_features']):
            continue
        else:
            hpo_str = row['present_features'].replace(';', ',')
        image_data = {'image_name': str(row['image_id']) + '.jpg',
                      'hpo': hpo_str,
                      'omim': int(row['omim']) if pd.notnull(row['omim']) else '',
                      'disorder': row['internal_syndrome_name']}
        input_images.append(image_data)

    return input_images


def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data has been saved to {filename}.")

def load_cached_file(cached_dir, name):
    file_path = os.path.join(cached_dir, name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        data = None

    return data
