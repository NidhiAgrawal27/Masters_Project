from operator import index
import argparse
import pathlib
from utilities import utils, dataframe_to_gml

CONFIG = {
    "generated_files": "../logs/generated_files/segregated_iota.gml",
    "data_path1": "../logs/generated_files/segregated_iota.csv",
    "data_path2": "../logs/generated_files/unique_addresses.csv"
    
}

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    args = parser.parse_args()

    file_name = CONFIG['generated_files']
    segregated_iota_df = CONFIG['data_path1']
    unique_addresses_df = CONFIG['data_path2'] 

    utils.set_seed(args.seed)

    dataframe_to_gml.convert_to_gml(file_name, segregated_iota_df, unique_addresses_df)

if __name__ == "__main__":
    main()