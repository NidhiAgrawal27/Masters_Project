import networkx as nx
import tqdm 
import numpy as np
# from sklearn.metrics import adjusted_mutual_info_score, homogeneity_score, rand_score, adjusted_rand_score, pair_confusion_matrix
from graph_tool import dynamics as gtd
import tqdm as tqdm
import graph_tool.topology as gtt
import graph_tool.all as gt
import pandas as pd
import csv
import networkx.algorithms.community as nx_comm
import itertools
from networkx.algorithms.community.centrality import girvan_newman

def gt2nx(g0):
  g = nx.Graph()
  for i,j in g0.edges():
    g.add_edge(i,j)
  return g

# graph_gt = gt.load_graph('/local/scratch/correspondence_network/part1_final_logs/btc_2012_logs/unweighted/h0_h1/generated_files/graph/btc_2012_h0_h1_graph.xml.gz')
# v = gtt.extract_largest_component(graph_gt, directed=None, prune=True)
# print("extract largest component number of addresses",v.num_vertices())
# G = gt2nx(v)

# nx.write_graphml(G, "btc_2012_h0_h1_component_graph_updated.graphml")

G = nx.read_graphml('/home/user/swaram/Masters_Project/girvan_newmann_heuristic/test/btc_2012_h0_h1_component_graph_updated.graphml')
print('*********************')
label_prop_comm = nx_comm.label_propagation_communities(G)
communities = [list(c) for c in label_prop_comm]
print(communities)
mod = nx_comm.modularity(G, communities)
# print("mod :", mod)
new_mod = mod
n = 2
modularity_list = []

while new_mod - mod <= 0:
    print('*************************')
    betweenness = nx.edge_betweenness_centrality(G)
    edge = max(betweenness, key=betweenness.get)
    G.remove_edge(*edge)
    if nx.number_connected_components(G) >= n:
        print(nx.number_connected_components(G))
        print("The graph has broken into two components after removing edge", edge)
        # break
        new_label_prop_comm = nx_comm.label_propagation_communities(G)
        new_communities = [list(c) for c in new_label_prop_comm]
        new_mod = nx_comm.modularity(G, new_communities)
        print(new_mod)
        modularity_list.append({'number_of_components' : n, 'New_modularity' : new_mod, 'Original_modularity' : mod})
        n += 1 

components = nx.connected_components(G)
components = list(components)

components_data = []
for i, component in enumerate(components):
    component_data = {"Component Number": i, "Nodes": component}
    components_data.append(component_data)

df = pd.DataFrame(components_data)
df.to_csv("components.csv",index=False)

keys = modularity_list[0].keys()

with open('Modularity.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(modularity_list)
    
nx.write_graphml(G, "btc_2012_h0_h1_finalized_graph.graphml")