import re

def parse_hpo(input_str):
    pattern = r'HP:\d{7}'
    matches = re.findall(pattern, input_str)
    return matches

def analyze_case_hpo(hpo_str, output_filename, get_ranked_list_fn, save_to_json_fn):
    data = get_ranked_list_fn(hpo_str)
    save_to_json_fn(data, output_filename)
    return data
