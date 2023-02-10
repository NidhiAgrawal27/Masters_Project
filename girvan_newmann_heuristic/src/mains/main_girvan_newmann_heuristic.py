import pandas as pd
import argparse
import pathlib
from utilities import set_seed, pathnames, visualization
import networkx as nx
import numpy as np
from sklearn.metrics import adjusted_mutual_info_score, homogeneity_score, rand_score, adjusted_rand_score, pair_confusion_matrix
from graph_tool import dynamics as gtd
import tqdm as tqdm
import graph_tool.topology as gtt
import graph_tool.all as gt
import graph_tool.centrality as gtc
import graph_tool.util as gtu
import csv
import networkx.algorithms.community as nx_comm
from networkx.algorithms.community.centrality import girvan_newman
import pickle

import warnings
warnings.filterwarnings('ignore')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    parser.add_argument("--weighted", type=str, help="Weighted graph: yes or no", required=True)
    args = parser.parse_args()

    set_seed.set_seed(args.seed)
    weighted = args.weighted

    PATHNAMES = pathnames.pathnames(weighted)
    pathlib.Path(PATHNAMES['generated_files']).mkdir(parents=True, exist_ok=True)
    pathlib.Path(PATHNAMES['figure_dir']).mkdir(parents=True, exist_ok=True)
    dir_generated_files = PATHNAMES['generated_files']
    fig_dir = PATHNAMES['figure_dir']
    # fig_dir = fig_dir 

    wt = 'unweighted'
    if weighted == 'yes':
        wt = 'weighted'
        # address_id_file = data_dir + '_' + heuristic + '_wt_address_ids.csv' 
        # edge_data_file = data_dir + '_' + heuristic + '_wt_edge_data.csv'
        fig_dir = fig_dir + '_wt_'

    print('\n\n*********************** Processing of ' + wt + ' initiated ***********************\n')    
    
    # df_edge_data = pd.read_csv(edge_data_file)
    addresses = pd.read_csv(PATHNAMES['address_ids'])
    df_gt = pd.read_csv(PATHNAMES['ground_truth_path'])
    # load the files and convert the graph
    print("Loading graph")
    graph_gt = gt.load_graph(PATHNAMES['graph'])
    print("Loading Vertex Properties")
    with open(PATHNAMES['vertex_property'], 'rb') as handle:
        vertex_property = pickle.load(handle)
        handle.close()
    
    entity_df = pd.merge(addresses, df_gt, left_on = "address", right_on = "address", how = "inner")
    entity_df = entity_df.drop('sector', axis=1)
    entity_df = entity_df.drop('id', axis=1)
    def compute_components(graph_of_correspondences, comps):
        components = {}
        comp_list = []

        print('\nCompute Components of Graph Progress Bar:')
        for i in tqdm.tqdm(range(graph_of_correspondences.num_vertices())):
            c = comps[i]
            if c not in components: components[c] = [i]
            else: components[c].append(i)
        print()

        print('Create Components List Progress Bar:')
        for c in tqdm.tqdm(components):
            comp_list.append({'component' : c, 'num_of_addrs' : len(components[c]), 'address_ids' : components[c]})

        return comp_list

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
    ent_df = pd.DataFrame(ent) #ent_df contains all the addresses component-wise that are present in the ground-truth, used later to get the entities of addresses after girvin newmann

    def gt2nx(g0):
        g = nx.Graph()
        for i,j in g0.edges():
            g.add_edge(i,j)
        return g

    def gt2nx1(g0, vertex_property):
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

    def extract_entities(df, addresses): #extracts the entities from the ent_df dataframe, takes less time than to compare with groundtruth, takes input lists of addresses, returns dictionary in the form-> address: entity
        result = {}
        for index, row in df.iterrows():
            for address in addresses:
                if address in row['addresses']:
                    result[address] = row['entity'][row['addresses'].index(address)]
        return result

    G = gt2nx1(graph_gt, vertex_property)

    def extract_subgraphs(G, df): #gives the component subgraphs of the original graph that have more than one entity
        subgraphs = []
        components = list(nx.connected_components(G))
        for component in tqdm.tqdm(components):
            entities = set(df[df['address'].isin(component)]['entity'].tolist())
            if len(entities) > 1:
                subgraph = G.subgraph(component)
                entity_count = len(entities)
                subgraphs.append((subgraph, entity_count))
        return subgraphs

    subgraphs = extract_subgraphs(G, df_gt)

    print('*********************************')

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
                G = gt2nx1(G_gt, vp_graph)

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
        visualization.plot_girvan_newmann_metrics(modularity_df['New_modularity'], "Iterations", 'Modularity', 'Girvin Newmann modularity mapping', visualization.uzh_colors, fig_dir)

        #save all csv files and graph
        modularity_df.to_csv(dir_generated_files + "Modularity.csv",index=False)
        sub_df = pd.DataFrame(subgraph_entities)
        sub_df.to_csv(dir_generated_files + "subgraph_entities_2_nodes.csv",index=False)
        result_lists_df = pd.DataFrame(result_lists)
        result_lists_df.to_csv(dir_generated_files + "component_data_df.csv",index=False)

        nx.write_graphml(G, dir_generated_files + "btc_2012_h0_h1_finalized_graph.graphml")
    
    print('\n\n*********************** Processing of ' + wt + ' completed ***********************\n')
    print()

if __name__ == "__main__":
    main()


