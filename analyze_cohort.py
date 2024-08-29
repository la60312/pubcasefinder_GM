import os
import requests
import argparse
import pandas as pd
from utils.api import analyze_image, get_pcf_ranked_list
from utils.evaluation import get_pcf_rank, get_gm_rank
from utils.hpo import analyze_case_hpo
from utils.general import (preprocess_jstage_metadata, preprocess_gmdb_metadata,
                           save_to_json, load_cached_file)

def main():
    parser = argparse.ArgumentParser(description="Request data from the PubCaseFinder API.")
    parser.add_argument('-m', '--metadata', type=str, default='jstage', help="The filename of the input metadata TSV file")
    parser.add_argument('--metadata_source', type=str, help="Metadata from jstage or gmdb.")
    parser.add_argument('--images_dir', type=str, help="Image input directory")
    parser.add_argument('--hpo_output_dir', type=str, help="Output directory")
    parser.add_argument('--gm_output_dir', type=str, help="Output directory")
    parser.add_argument('--hpo_cache_dir', type=str, required=False, help="Use previous HPO cached data in cached directory")
    parser.add_argument('--gm_cache_dir', type=str, required=False, help="Use previous GestaltMatcher cached data in cached directory")
    parser.add_argument('--gm_url', default='localhost', dest='gm_url', help='URL to the API.')
    parser.add_argument('--gm_port', default=5000, dest='gm_port', help='Port to the API.')

    args = parser.parse_args()

    gm_predict_URL = f"http://{args.gm_url}:{args.gm_port}/predict"
    auth = requests.auth.HTTPBasicAuth('your_username', 'your_password')

    hpo_cache_dir = args.hpo_cache_dir
    hpo_output_dir = args.hpo_output_dir
    gm_cache_dir = args.gm_cache_dir
    gm_output_dir = args.gm_output_dir

    if hpo_cache_dir:
        print('Use HPO cached data from cached directory.')
    if not os.path.exists(hpo_output_dir):
        os.makedirs(hpo_output_dir)

    if gm_cache_dir:
        print('Use GestaltMatcher cached data from cached directory.')
    if not os.path.exists(gm_output_dir):
        os.makedirs(gm_output_dir)

    if args.metadata_source == 'jstage':
        # jstage metadata format
        input_images = preprocess_jstage_metadata(args.metadata)
    else:
        # GMDB metadata format
        input_images = preprocess_gmdb_metadata(args.metadata)
    print(len(input_images))

    output_data = []
    for image_data in input_images:
        file_name = f"{image_data['image_name'].split('.')[0]}.json"
        output_filename = os.path.join(hpo_output_dir, file_name)

        #if hpo_cache_dir:
        if os.path.exists(os.path.join(hpo_cache_dir, file_name)):
            hpo_data = load_cached_file(hpo_cache_dir, file_name)
        else:
            hpo_data = analyze_case_hpo(image_data['hpo'], output_filename, get_pcf_ranked_list, save_to_json)

        if gm_cache_dir:
            gm_data = load_cached_file(gm_cache_dir, file_name)
        else:
            input_file = os.path.join(args.images_dir, image_data['image_name'])
            if os.path.exists(input_file):
                gm_data = analyze_image(input_file, gm_output_dir, gm_predict_URL, auth)

        image_data['hpo_rank'] = get_pcf_rank(hpo_data, image_data['omim'])
        image_data['gm_rank'] = get_gm_rank(gm_data['suggested_syndromes_list'], image_data['omim']) if gm_data else 0
        output_data.append(image_data)

    output_df = pd.DataFrame(output_data)
    output_df = output_df[['image_name', 'hpo_rank', 'gm_rank', 'disorder', 'omim', 'hpo']]
    output_df.to_csv('results.tsv', index=False, sep='\t')

if __name__ == '__main__':
    main()
