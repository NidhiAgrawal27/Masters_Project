import pandas as pd
import os
import argparse
import pathlib
import tqdm as tqdm
import pickle
import csv
import warnings
warnings.filterwarnings('ignore')

import graph_tool.all as gt
import graph_tool.centrality as gtc
import graph_tool.util as gtu

import networkx as nx
import networkx.algorithms.community as nx_comm

from utilities import set_seed, pathnames
from utilities.visualization import plot_girvan_newmann_metrics
from utilities.gt2nx import gt2nx
from utilities.nx2gt import nx2gt
from utilities.extract_subgraphs import extract_subgraphs
from utilities.get_address_labels import get_address_labels


def main(cur, heuristic, wt, PATHNAMES, data_dir, graph_data_dir, dir_generated_files, fig_dir):
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    args = parser.parse_args()

    set_seed.set_seed(args.seed)

    address_id_file = data_dir + '_' + heuristic + '_address_ids.csv'
    graph_file = graph_data_dir + '_' + heuristic + '_graph.xml.gz'
    vertex_property_file = graph_data_dir + '_' + heuristic + '_vertex_prop.pickle'

    if wt == 'weighted':
        address_id_file = data_dir + '_' + heuristic + '_wt_address_ids.csv'
        graph_file = graph_data_dir + '_' + heuristic + '_wt_graph.xml.gz'
        vertex_property_file = graph_data_dir + '_' + heuristic + '_wt_vertex_prop.pickle'
        dir_generated_files = dir_generated_files + 'wt_'
        fig_dir = fig_dir + 'wt_'    
    
    addresses = pd.read_csv(address_id_file)
    df_gt = pd.read_csv(PATHNAMES['ground_truth_path'])

    # load the files and convert the graph
    print("Loading graph...")
    graph_gt = gt.load_graph(graph_file)
    print("Loading Vertex Properties...")
    with open(vertex_property_file, 'rb') as handle:
        vertex_property = pickle.load(handle)
        handle.close()
    
    entity_df = pd.merge(addresses, df_gt, left_on = "address", right_on = "address", how = "inner")
    entity_df = entity_df.drop('sector', axis=1)
    entity_df = entity_df.drop('id', axis=1)

    # convert graph tool graph to a networkx graph
    G = gt2nx(graph_gt, vertex_property)

    # extract the required components from the graph
    subgraphs = extract_subgraphs(G, entity_df)
    subgraph_index = -1

    for subgraph_and_num_entities in subgraphs:
        subgraph_index += 1
        G = subgraph_and_num_entities[0]
        num_entities = subgraph_and_num_entities[1]

        if num_entities>=2:
            print("The number of entities in the subgraph-{} are {}".format(subgraph_index, num_entities))

            # common addresses in the ground truth
            sub_addresses = pd.DataFrame({"address":list(G.nodes())})
            df_common_gt = pd.merge(sub_addresses,entity_df,left_on="address",right_on="address")

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

            total_entities = len(set(df_common_gt["entity"]))
            while comm_split <= total_entities:
                # print('comm_split, total_entities: ', comm_split, total_entities)
                
                _,edge_betweenness = gtc.betweenness(G_gt)
                
                try:
                    # print('Splitting multiple edges at the same time')
                    edge = gtu.find_edge_range(G_gt, edge_betweenness, [sorted(edge_betweenness)[-10],max(edge_betweenness)])
                except:
                    try:
                        # print('Splitting single edge at a time')
                        edge = gtu.find_edge(G_gt, edge_betweenness, max(edge_betweenness))
                    except:
                        print('Continue the loop for next subgraph')
                        total_entities = -1
                        continue

                for e in edge:
                    split += 1
                    G_gt.remove_edge(e)
                G = gt2nx(G_gt, vp_graph)
                
                if nx.number_connected_components(G) >= n:
                    comm_split+=1
                    print("The graph has now {} components after removing edges.".format(nx.number_connected_components(G)))
                    print("The graph has broken after {} edge removals".format(split))
                    # break
                    new_label_prop_comm = nx_comm.label_propagation_communities(G)
                    new_communities = [list(c) for c in new_label_prop_comm]
                    new_mod = nx_comm.modularity(G, new_communities)
                    print(new_mod)

                    # get labels of the addresses
                    predicted_entity_labels = get_address_labels(G, df_common_gt)

                    count_of_true_entity_labels = len([value for key,value in predicted_entity_labels.items() if value!="Unknown"])
                    
                    # # add other metrics here like the ARI, AMI, etc. here # #
                    
                    modularity_list.append({
                                            'total edge splits':split, 
                                            'total component splits':comm_split, 
                                            'number_of_components' : nx.number_connected_components(G), 
                                            'new_modularity' : new_mod, 
                                            'original_modularity' : mod, 
                                            "count_of_known_entites": count_of_true_entity_labels,
                                            'subgraph_index': subgraph_index
                                        })
                    n = nx.number_connected_components(G)+1
                    G_gt, vp_graph = nx2gt(G)

                    # #compare separated components with the ground truth and verify that they split into same entity comps # #
            
            if total_entities == -1: continue

            ### graphs to be plotted after exiting the while loop ###
            # modularity change vs component splits
            # AMI, ARI, homogeneity change vs component splits
            # number of communities vs component split
            # graph showing the change in increasing address validation

            modularity_df = pd.DataFrame(modularity_list)
            modularity_df.to_csv(dir_generated_files + 'comp_'+ str(subgraph_index) +'_modularity.csv',index=False)

            plot_girvan_newmann_metrics(
                                            modularity_df['new_modularity'].index, 
                                            modularity_df['new_modularity'], 
                                            "Iterations", 
                                            'Modularity', 
                                            'Girvin Newmann Modularity Mapping', 
                                            'blue', 
                                            fig_dir + 'comp_'+ str(subgraph_index) +'_modularity.png'
                                        )
            plot_girvan_newmann_metrics(
                                            modularity_df['count_of_known_entites'].index, 
                                            modularity_df['count_of_known_entites'], 
                                            "Iterations", 
                                            'count of addresses with known entities', 
                                            'Girvin Newmann count of known entites Mapping \
                                            \n Num of unique entities in the component-{} are {} \
                                            \n Total num of addresses in the component-{} are {}'.format(subgraph_index, num_entities, df_common_gt.shape[0], num_entities), 
                                            'red', 
                                            fig_dir + 'comp_'+ str(subgraph_index) +'_count_of_known_entites.png'
                                        )

    print('\n\n*********************** Processing of ' + cur + ' ' + wt + ' completed ***********************\n')
    print()

if __name__ == "__main__":

    cur = 'btc_2012'
    heuristic = 'h0_h1'
    weighted = ['unweighted', 'weighted']

    for i in range(13): # num of bitcoin files which have 14 days data each
        cur = 'btc_2012_' + str(i)
        for wt in weighted:
            
            print('\n\n*********************** Processing of ' + cur + ' ' + wt + ' initiated ***********************\n')

            PATHNAMES = pathnames.pathnames(cur, heuristic, wt)
            pathlib.Path(PATHNAMES['generated_files']).mkdir(parents=True, exist_ok=True)
            pathlib.Path(PATHNAMES['figure_dir']).mkdir(parents=True, exist_ok=True)
            dir_generated_files = PATHNAMES['generated_files']
            fig_dir = PATHNAMES['figure_dir']

            dir_generated_files = dir_generated_files + cur + '_' + heuristic + '_'
            fig_dir = fig_dir + cur + '_' + heuristic + '_'

            data_path = PATHNAMES['data_path']

            # # local data path (comment server path below when using local path)
            # data_dir = data_path + cur + '/' + cur
            # graph_data_dir = data_path + cur + '/' + cur

            # server data path (comment local path above when using server path)
            data_dir = data_path + cur + '_logs/' + wt + '/' + heuristic + '/generated_files/' + cur
            graph_data_dir = data_path + cur + '_logs/' + wt + '/' + heuristic + '/generated_files/graph/' + cur

            main(cur, heuristic, wt, PATHNAMES, data_dir, graph_data_dir, dir_generated_files, fig_dir)


