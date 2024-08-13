import logging
import yaml
from etl.extract import Extractor
from etl.transform import Transformer
from etl.load import Loader
from etl.utils import setup_logging
import pandas as pd

# Setup logging
setup_logging()

# Load configuration
with open("config/config.yaml", 'r') as config_file:
    config = yaml.safe_load(config_file)

def main():
    # Extract
    extractor = Extractor(config['google_maps_api_key'])
    raw_data = extractor.fetch_all_places(config['location'], config['radius'])
    pd.DataFrame(raw_data).to_csv("data/raw/vet_clinics.csv")

    # Transform
    transformer = Transformer(config['location'])  # Pass base_location from config
    transformed_data = transformer.process(raw_data)
    
    
    # Load
    loader = Loader(config['duckdb']['database'])
    loader.to_duckdb(transformed_data)

    logging.info("ETL process completed successfully.")

if __name__ == "__main__": 
    main()