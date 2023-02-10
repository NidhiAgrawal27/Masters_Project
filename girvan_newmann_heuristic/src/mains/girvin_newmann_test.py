import networkx as nx
import tqdm 
import numpy as np
# from sklearn.metrics import adjusted_mutual_info_score, homogeneity_score, rand_score, adjusted_rand_score, pair_confusion_matrix
from graph_tool import dynamics as gtd
import tqdm as tqdm
import graph_tool.topology as gtt
import graph_tool.all as gt
import graph_tool.centrality as gtc
import graph_tool.util as gtu
import pandas as pd
import csv
import networkx.algorithms.community as nx_comm
import itertools
from networkx.algorithms.community.centrality import girvan_newman
import pickle

def gt2nx(g0, vertex_property):
    g = nx.Graph()
    for i,j in g0.edges():
        if not vertex_property[i] in g.nodes():
            g.add_node(vertex_property[i])
        if not vertex_property[j] in g.nodes():
            g.add_node(vertex_property[j])
        g.add_edge(vertex_property[i],vertex_property[j])
    return g

def nx2gt(g0):
    mp = dict()
    g = nx.Graph()
    for i,j in g0.edges():
        if i not in mp:
            mp[i] = len(mp)
        if j not in mp:
            mp[j] = len(mp)
        g.add_edge(mp[i],mp[j])
    ggt = gt.Graph()
    vertex_property = ggt.new_vertex_property("object")
    mpi = {value:key for key,value in mp.items()}
    for i,j in g.edges():
        ggt.add_edge(i,j,add_missing = True)
    for i in ggt.vertices():
        vertex_property[i] = mpi[i]
    return ggt, vertex_property

def get_address_labels(nx_graph, local_ground_truth_data):
    entity = {}
    nx.set_node_attributes(nx_graph, entity, "entity")
    for comp in nx.connected_component_subgraph(nx_graph):
        list_of_addrs = pd.DataFrame([vertex for vertex in comp.nodes()], columns = ["address"])
        num_entities = list(pd.merge(list_of_addrs,local_ground_truth_data,left_on="address",right_on="address")['entity'])
        if len(set(num_entities)) == 1:
            for nodename in comp.nodes():
                entity[nodename] = num_entities[0]
        else:
            for nodename in comp.nodes():
                entity[nodename] = "Unknown"
                # # one solution
                # max_entity = num_entities.value_counts().index.tolist()[0]
                # entity[nodename] = max_entity
    
    return entity

# load the files and convert the graph
print("Loading graph")
graph_gt = gt.load_graph('/local/scratch/correspondence_network/Girvin_Newmann_data/btc_2012_logs/btc_2012_0_logs/unweighted/h0_h1/generated_files/graph/btc_2012_0_h0_h1_graph.xml.gz')
print("Loading Vertex Properties")
with open('/local/scratch/correspondence_network/Girvin_Newmann_data/btc_2012_logs/btc_2012_0_logs/unweighted/h0_h1/generated_files/graph/btc_2012_0_h0_h1_vertex_prop.pickle', 'rb') as handle:
    vertex_property = pickle.load(handle)
    handle.close()
df_gt = pd.read_csv("/local/scratch/correspondence_network/NS_Project/ns21fp/data/ground_truth_id.csv")
G = gt2nx(graph_gt, vertex_property)

# Get the largest connected component
G = max([G.subgraph(c).copy() for c in nx.connected_components(G)],key=len)
nodes_largest = pd.DataFrame({"address":list(G.nodes())})
df_common_gt = pd.merge(nodes_largest,df_gt,left_on="address",right_on="address")
total_entities = len(set(df_common_gt["entity"]))

print('*************************')

label_prop_comm = nx_comm.label_propagation_communities(G)
communities = [list(c) for c in label_prop_comm]
# print(communities)
mod = nx_comm.modularity(G, communities)
print("mod :", mod)
new_mod = mod
n = 2
modularity_list = []
G_gt,vp_graph = nx2gt(G)
split = 0       # total edges being removed
comm_split = 0  # total number of times the component split after removing the edges

# change the while condition as this is not properly terminating.
# maybe keep it to a certain number of splits- eg: 10 component splits, 15 component splits, etc.

while comm_split <= total_entities:
    split += 1
    _,edge_betweenness = gtc.betweenness(G_gt)
    # edge = gtu.find_edge(G_gt, edge_betweenness, max(edge_betweenness))  # for splitting only one edge at once
    edge = gtu.find_edge_range(G_gt, edge_betweenness, [sorted(edge_betweenness)[-10],max(edge_betweenness)])   # for splitting multiple edges at the same time
    for e in edge:
        G_gt.remove_edge(e)
    G = gt2nx(G_gt, vp_graph)
    
    if nx.number_connected_components(G) >= n:
        comm_split+=1
        print("The graph has broken into two components after removing edge")
        print("The graph has broken after {} splits".format(split))
        # break
        new_label_prop_comm = nx_comm.label_propagation_communities(G)
        new_communities = [list(c) for c in new_label_prop_comm]
        new_mod = nx_comm.modularity(G, new_communities)
        print(new_mod)

        # get labels of the addresses
        entity_labels = get_address_labels(G, df_common)
        
        # # add other metrics here like the ARI, AMI, etc. here # #
        
        modularity_list.append({'total edge splits':split, 'total component splits':comm_split, 'number_of_components' : nx.number_connected_components(G), 'New_modularity' : new_mod, 'Original_modularity' : mod})
        n = nx.number_connected_components(G)+1

        # #compare the separated components with the ground truth and verify that they are splitting into the same entity components ##

### graphs to be plotted after exiting the while loop ###
# modularity change vs component splits
# AMI, ARI, homogeneity change vs component splits
# number of communities vs component split

components = nx.connected_components(G)
components = list(components)

components_data = []
for i, component in enumerate(components):
    component_data = {"Component Number": i, "Nodes": component}
    components_data.append(component_data)

df = pd.DataFrame(components_data)
# df.to_csv("components.csv",index=False)

keys = modularity_list[0].keys()

with open('Modularity.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(modularity_list)
    
# nx.write_graphml(G, "btc_2012_h0_h1_finalized_graph.graphml")