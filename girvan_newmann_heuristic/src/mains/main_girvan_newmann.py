import pandas as pd
import numpy as np
import argparse
import pathlib
import tqdm as tqdm
import pickle
import warnings
warnings.filterwarnings('ignore')

# from sklearn.metrics import adjusted_mutual_info_score, homogeneity_score, rand_score, adjusted_rand_score, pair_confusion_matrix

import graph_tool.topology as gtt
import graph_tool.all as gt
import graph_tool.centrality as gtc
import graph_tool.util as gtu
# from graph_tool import dynamics as gtd

import networkx as nx
import networkx.algorithms.community as nx_comm
# from networkx.algorithms.community.centrality import girvan_newman

from utilities import set_seed, pathnames
from utilities.visualization import plot_girvan_newmann_metrics
from utilities.compute_components import compute_components
from utilities.gt2nx import gt2nx
from utilities.nx2gt import nx2gt
from utilities.extract_entities import extract_entities
from utilities.extract_subgraphs import extract_subgraphs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    parser.add_argument("--currency", type=str, help="currency name example - btc: Bitcoin, iota: IoTa", required=True)
    parser.add_argument("--heuristic", type=str, help="name of heuristic, example: h0, or h0_h1", required=True)
    parser.add_argument("--weighted", type=str, help="Weighted graph: yes or no", required=True)
    args = parser.parse_args()

    set_seed.set_seed(args.seed)
    cur = args.currency
    heuristic = args.heuristic
    weighted = args.weighted

    PATHNAMES = pathnames.pathnames(cur, heuristic, weighted)
    pathlib.Path(PATHNAMES['generated_files']).mkdir(parents=True, exist_ok=True)
    pathlib.Path(PATHNAMES['figure_dir']).mkdir(parents=True, exist_ok=True)
    dir_generated_files = PATHNAMES['generated_files']
    fig_dir = PATHNAMES['figure_dir']

    dir_generated_files = dir_generated_files + cur + '_' + heuristic + '_'
    fig_dir = fig_dir + cur + '_' + heuristic + '_'

    data_path = PATHNAMES['data_path']
    data_dir = data_path + cur + '/' + cur

    address_id_file = data_dir + '_' + heuristic + '_address_ids.csv'
    graph_file = data_dir + '_' + heuristic + '_graph.xml.gz'
    vertex_property_file = data_dir + '_' + heuristic + '_vertex_prop.pickle'

    wt = 'unweighted'
    if weighted == 'yes':
        wt = 'weighted'
        address_id_file = data_dir + '_' + heuristic + '_wt_address_ids.csv'
        graph_file = data_dir + '_' + heuristic + '_wt_graph.xml.gz'
        vertex_property_file = data_dir + '_' + heuristic + '_wt_vertex_prop.pickle'
        dir_generated_files = dir_generated_files + '_wt_'
        fig_dir = fig_dir + '_wt_'


    print('\n\n*********************** Processing of ' + cur + ' ' + wt + ' initiated ***********************\n')    
    
    addresses = pd.read_csv(address_id_file)
    df_gt = pd.read_csv(PATHNAMES['ground_truth_path'])

    # load the files and convert the graph
    print("Loading graph")
    graph_gt = gt.load_graph(graph_file)
    print("Loading Vertex Properties")
    with open(vertex_property_file, 'rb') as handle:
        vertex_property = pickle.load(handle)
        handle.close()
    
    entity_df = pd.merge(addresses, df_gt, left_on = "address", right_on = "address", how = "inner")
    entity_df = entity_df.drop('sector', axis=1)
    entity_df = entity_df.drop('id', axis=1)

    c, _ = gtt.label_components(graph_gt)
    ccc = compute_components(graph_gt, c)

    ent = []
    for i in tqdm.tqdm(range(len(ccc))):
        t = pd.DataFrame.from_dict(ccc[i])
        com_ent = pd.merge(t, entity_df, left_on = "address_ids", right_on = "address_id", how = "inner")
        num_entities = len(np.unique(com_ent['entity']))
        component= np.unique(com_ent['component'])
        if not com_ent.empty:
            ent.append({'number_entities': num_entities,'component' : component, 'addresses_ids' : list(com_ent['address_ids']), 'addresses' : list(com_ent['address']), 'entities' : list(com_ent['entity'])})
    ent_df = pd.DataFrame(ent) 
    #ent_df contains all the addresses component-wise that are present in the ground-truth, 
    # used later to get the entities of addresses after girvin newmann

    G = gt2nx(graph_gt, vertex_property)
    subgraphs = extract_subgraphs(G, df_gt)

    for subgraph_and_num_entities in subgraphs:
        G = subgraph_and_num_entities[0]
        num_entities = subgraph_and_num_entities[1]
        subgraph_entities = []
        if len(G) == 2: #if the subgraph has only 2 nodes, save the addresses with their entities in a list  
            node1, node2 = G.nodes()
            node_list = [node1, node2]
            result = extract_entities(ent_df, node_list)
            subgraph_entities.append(result)
        
        else:
            label_prop_comm = nx_comm.label_propagation_communities(G)
            communities = [list(c) for c in label_prop_comm]
            mod = nx_comm.modularity(G, communities)
            print("mod :", mod)
            new_mod = mod
            n = 2
            modularity_list = []
            G_gt,vp_graph = nx2gt(G)
            split = 0       # total edges being removed
            comm_split = 0  # total number of times the component split after removing the edges
            # num_entities = 2
            while comm_split <= num_entities:
                split += 1
                _,edge_betweenness = gtc.betweenness(G_gt)
                # edge = gtu.find_edge(G_gt, edge_betweenness, max(edge_betweenness))  # for splitting only one edge at once
                edge = gtu.find_edge_range(G_gt, edge_betweenness, [sorted(edge_betweenness)[-10],max(edge_betweenness)])   
                for e in edge:
                    G_gt.remove_edge(e)
                G = gt2nx(G_gt, vp_graph)

                if nx.number_connected_components(G) >= n:
                    comm_split+=1
                    print("The graph has broken into two components after removing edge")
                    print("The graph has broken after {} splits".format(split))
                    new_label_prop_comm = nx_comm.label_propagation_communities(G)
                    new_communities = [list(c) for c in new_label_prop_comm]
                    new_mod = nx_comm.modularity(G, new_communities)
                    n = nx.number_connected_components(G)+1
                # mt
                    modularity_list.append({'total edge splits':split, 'total component splits':comm_split, 'number_of_components' : nx.number_connected_components(G), 'New_modularity' : new_mod, 'Original_modularity' : mod})
                        
                    
        modularity_df = pd.DataFrame(modularity_list)
        result_lists = []
        components_ = nx.connected_components(G)
        components_ = list(components_)
        for compts in components_: #gives the entities of addresses in different components
            result = extract_entities(ent_df, compts)
            result_lists.append({'component_addresses': compts,'entities' : result_lists})
            
        # plot modularity
        plot_girvan_newmann_metrics(modularity_df['New_modularity'].index, modularity_df['New_modularity'], "Iterations", 'Modularity', 'Girvin Newmann Modularity Mapping', 'blue', fig_dir + 'modularity.png')

        #save all csv files and graph
        modularity_df.to_csv(dir_generated_files + "modularity.csv",index=False)
        sub_df = pd.DataFrame(subgraph_entities)
        sub_df.to_csv(dir_generated_files + "subgraph_entities_to_nodes.csv",index=False)
        result_lists_df = pd.DataFrame(result_lists)
        result_lists_df.to_csv(dir_generated_files + "components.csv",index=False)

        nx.write_graphml(G, dir_generated_files + "finalized_graph.graphml")
    
    print('\n\n*********************** Processing of ' + cur + ' ' + wt + ' completed ***********************\n')
    print()

if __name__ == "__main__":
    main()


