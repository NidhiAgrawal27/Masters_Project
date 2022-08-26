import pandas as pd
import numpy as np
from igraph import Graph
import networkx as nx
from utilities import utils

heuristics = ["h0", "h1", "h0 and h1", "h0 or h1"]


def Clustering(file):
    print('\n')
    print("CLUSTERING")
    for  i in heuristics:
        df = pd.read_csv(file)
        df = df[df[i] == 1]
        edge_tuples = df[["id_input_addresses_x", "id_output_addresses_y"]].itertuples(index=False)
        g = Graph.TupleList(edge_tuples, directed=False, weights=False)

        cs = g.community_label_propagation()
        cs_addr = sorted([g.vs.select(c)["name"] for c in cs], key=len)
        cs_sizes = [len(cs)]

        print(i,"- Number of Clusters:",cs_sizes)
        print ("Addresses belonging to cluster:",cs_addr)
        print('\n')