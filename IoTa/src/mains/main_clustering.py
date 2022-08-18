import pandas as pd
import argparse
import pathlib
from igraph import Graph
import networkx as nx
from utilities import utils, clustering

CONFIG = utils.pathnames()

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    args = parser.parse_args()

    utils.set_seed(args.seed)

    heuristics=pd.read_csv(CONFIG["heuristics"])
    
    h0 = "h0"
    h1 = "h1"

    #applying the clustering to the segregated data file
    heuristics.apply(lambda x: clustering.Clustering(x.h0,x.h1,heuristics).implement_clustering(heuristics), axis=1)
    
    heuristics['h0 & h1'] = heuristics['h0 & h1'].astype(int)
    heuristics['h0 or h1'] = heuristics['h0 or h1'].astype(int)
    heuristics.to_csv(CONFIG["heuristics"], index=False)

    #creating graph
    #edge_tuples = heuristics[["id_input_addresses_x", "id_output_addresses_y", "h0 & h1"]].itertuples(index=False)
    #g = Graph.TupleList(edge_tuples, directed=False, weights=True)
    

    #cs = g.community_label_propagation()

    #cs_addr = sorted([g.vs.select(c) for c in cs], key=len)

    #cs_size = len(cs)

    #print (cs_size, cs_addr)

if __name__ == "__main__":
    main()