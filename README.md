# PubCaseFinder API Data Request Script

This script is used to request and analyze data from the PubCaseFinder API. It processes metadata from a TSV file, manages image directories, and caches data for HPO and GestaltMatcher analysis.

## Prerequisites

- Python 3.x
- Required Python packages:
  - `argparse`
  - `requests`
  - `pandas`

## Usage

### Command-line Arguments

The script accepts several command-line arguments to configure the input, output, and API details.

| Argument            | Type   | Required | Description                                                                                      |
|---------------------|--------|----------|--------------------------------------------------------------------------------------------------|
| `-m, --metadata`    | string | Yes      | The filename of the input metadata TSV file.                                                     |
| `--metadata_source` | string | Yes      | Specifies the source of the metadata. It can be either jstage or gmdb.                           |
| `--images_dir`      | string | Yes      | Directory containing the input images.                                                           |
| `--hpo_output_dir`  | string | Yes      | Directory where the HPO analysis output will be stored.                                          |
| `--gm_output_dir`   | string | Yes      | Directory where the GestaltMatcher analysis output will be stored.                               |
| `--hpo_cache_dir`   | string | No       | Directory containing cached HPO data. If provided, the script will use cached data.              |
| `--gm_cache_dir`    | string | No       | Directory containing cached GestaltMatcher data. If provided, the script will use cached data.   |
| `--gm_url`          | string | No       | URL to the GestaltMatcher API. Default is `localhost`.                                           |
| `--gm_port`         | int    | No       | Port for the GestaltMatcher API. Default is `5000`.                                              |

### Example Usage

To run the script with the necessary arguments, use the following command:

```bash
python analyze_cohort.py --metadata image_metadata_bh24.tsv --hpo_output_dir hpo_output --gm_output_dir gm_output --images_dir bh24 --gm_url 127.0.0.1 --gm_port 5001
```

### Argument Details

- **`--metadata`**: This is the TSV file containing metadata about the images. The script uses this file to fetch relevant information for analysis.
  
- **`--metadata_source`**: (str) Specifies the source of the metadata. It can be either jstage or gmdb.
- 
- **`--images_dir`**: The directory where the images to be analyzed are stored. The script will process these images according to the metadata provided.

- **`--hpo_output_dir`**: Specifies the output directory for the HPO analysis results. The script will save the results of the HPO analysis here.

- **`--gm_output_dir`**: Specifies the output directory for the GestaltMatcher analysis results. The results from the GestaltMatcher will be stored here.

- **`--hpo_cache_dir`**: Optional. If you have previously cached HPO data, you can specify the directory here. The script will use this data to speed up processing.

- **`--gm_cache_dir`**: Optional. Similar to the HPO cache, this allows you to use previously cached GestaltMatcher data.

- **`--gm_url`**: The URL of the GestaltMatcher API. By default, it is set to `localhost`, but you can specify a different URL if the API is hosted elsewhere.

- **`--gm_port`**: The port on which the GestaltMatcher API is running. The default port is `5000`, but you can change it if needed.

### Example Command Breakdown

#### Analyze jstage test set 
```bash
python analyze_cohort.py \
    --metadata image_metadata_bh24.tsv \
    --metadata_source jstage \
    --hpo_output_dir hpo_output \
    --gm_output_dir gm_output \
    --images_dir bh24 \
    --gm_url 127.0.0.1 \
    --gm_port 5001
```

- **`--metadata image_metadata_bh24.tsv`**: Specifies `image_metadata_bh24.tsv` as the input metadata file.
- **`--metadata_source jstage`**: Specifies `jstage` as the input metadata source format.
- **`--hpo_output_dir hpo_output`**: The HPO analysis results will be stored in the `hpo_output` directory.
- **`--gm_output_dir gm_output`**: The GestaltMatcher analysis results will be stored in the `gm_output` directory.
- **`--images_dir bh24`**: The script will look for images in the `bh24` directory.
- **`--gm_url 127.0.0.1`**: The GestaltMatcher API is hosted on `127.0.0.1`.
- **`--gm_port 5001`**: The GestaltMatcher API is running on port `5001`.

If you already analyze the HPO and image already and the results are stored in hpo_output and gm_output, you can use the cache to speed up the analysis. 


#### Analyze jstage test set 
```bash
python analyze_cohort.py \
    --metadata image_metadata_bh24.tsv \
    --metadata_source jstage \
    --hpo_output_dir hpo_output \
    --gm_output_dir gm_output \
    --hpo_cache_dir hpo_output \
    --gm_cache_dir gm_output \
    --images_dir bh24 \
    --gm_url 127.0.0.1 \
    --gm_port 5001
```

#### Analyze gmdb test set 
```bash
python analyze_cohort.py \
    --metadata gmdb_frequent_test_metadata.tsv \
    --metadata_source gmdb \
    --hpo_output_dir hpo_output_gmdb \
    --gm_output_dir gm_output_gmdb \
    --images_dir gm_frequent_test_images \
    --gm_url 127.0.0.1 \
    --gm_port 5001
```

Use the cache to speed up the analysis.
```bash
python analyze_cohort.py \
    --metadata gmdb_frequent_test_metadata.tsv \
    --metadata_source gmdb \
    --hpo_output_dir hpo_output_gmdb \
    --gm_output_dir gm_output_gmdb \
    --hpo_cache_dir hpo_output_gmdb \
    --gm_cache_dir gm_output_gmdb \
    --images_dir gm_frequent_test_images \
    --gm_url 127.0.0.1 \
    --gm_port 5001
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
