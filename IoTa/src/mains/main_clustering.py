import pandas as pd
import argparse
import pathlib
from utilities import utils, clustering

PATHNAMES = utils.pathnames()

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    args = parser.parse_args()

    utils.set_seed(args.seed)

    file = PATHNAMES["heuristics"]
    clustering.Clustering(file)

if __name__ == "__main__":
    main()