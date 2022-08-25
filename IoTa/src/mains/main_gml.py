from operator import index
import argparse
import pathlib
from utilities import utils, dataframe_to_gml

PATHNAMES = utils.pathnames()

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    args = parser.parse_args()

    segregated_data_gml = PATHNAMES['segregated_data_gml']
    segregated_data_df = PATHNAMES['segregated_data']
    unique_addresses_df = PATHNAMES['addresses_data'] 

    utils.set_seed(args.seed)

    dataframe_to_gml.convert_to_gml(segregated_data_gml, segregated_data_df, unique_addresses_df)

if __name__ == "__main__":
    main()
