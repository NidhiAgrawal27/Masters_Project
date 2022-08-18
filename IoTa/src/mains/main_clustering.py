import pandas as pd
import argparse
import pathlib
from igraph import *
import networkx as nx
from utilities import utils, clustering

CONFIG = {
    "segregated_iota": "../logs/generated_files/segregated_iota.csv"
}

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    args = parser.parse_args()

    utils.set_seed(args.seed)

    segregated_iota=pd.read_csv(CONFIG["segregated_iota"])
    
    h0 = "h0"
    h1 = "h1"

    #applying the clustering to the segregated data file
    segregated_iota.apply(lambda x: clustering.Clustering(x.h0,x.h1,segregated_iota).implement_clustering(segregated_iota), axis=1)
    
    segregated_iota['h0 & h1'] = segregated_iota['h0 & h1'].astype(int)
    segregated_iota['h0 or h1'] = segregated_iota['h0 or h1'].astype(int)
    
    segregated_iota.to_csv(CONFIG["segregated_iota"], index=False)


if __name__ == "__main__":
    main()