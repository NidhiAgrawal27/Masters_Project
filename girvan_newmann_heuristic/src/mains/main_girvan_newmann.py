import pandas as pd
import numpy as np
import argparse
import pathlib
import tqdm as tqdm
import pickle
import warnings
warnings.filterwarnings('ignore')

import graph_tool.all as gt
import graph_tool.centrality as gtc
import graph_tool.util as gtu
import graph_tool.dynamics as gtd
import graph_tool.generation as gtg
import graph_tool.inference as gti
import graph_tool.topology as gtt

import networkx as nx
import networkx.algorithms.community as nx_comm

from sklearn.metrics import adjusted_mutual_info_score, homogeneity_score, rand_score, pair_confusion_matrix

from utilities import set_seed, pathnames
from utilities.visualization import plot_girvan_newmann_metrics
from utilities.gt2nx import gt2nx
from utilities.nx2gt import nx2gt
from utilities.extract_subgraphs import extract_subgraphs
from utilities.get_address_labels import get_address_labels
from utilities.label_propagation import label_prop


def main(idx, cur, heuristic, wt, PATHNAMES, data_dir, graph_data_dir, dir_generated_files, fig_dir):
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

        if num_entities>=2 and G.number_of_edges()>G.number_of_nodes():
            print("The number of entities in the subgraph-{} are {}".format(subgraph_index, num_entities))

            # common addresses in the ground truth
            sub_addresses = pd.DataFrame({"address":list(G.nodes())})
            # df_local_gt = pd.merge(sub_addresses,entity_df,left_on="address",right_on="address", how = "outer")
            # df_local_gt['entity'] = df_local_gt['entity'].fillna('Unknown')

            df_common_gt = pd.merge(sub_addresses,entity_df,left_on="address",right_on="address")
            G_gt,vp_graph = nx2gt(G)

            # label_prop_comm = nx_comm.label_propagation_communities(G)
            # communities = [list(c) for c in label_prop_comm]
            # mod = nx_comm.modularity(G, communities)

            communities = label_prop(G_gt,20)
            comp_comm = len(set(communities.fa))  # total number of communities
            mod = gti.modularity(G_gt,communities)
            print("mod :", mod)
            new_mod = mod
            n = 2
            modularity_list = []
            split = 0       # total edges being removed
            comm_split = 0  # total number of times the component split after removing the edges

            # initial true labels
            df_true_pred_labels = pd.merge(sub_addresses, entity_df, left_on = "address", right_on = "address", how = "outer")
            df_true_pred_labels['entity'] = df_true_pred_labels['entity'].fillna('Unknown')
            df_true_pred_labels.drop(['address_id'], axis=1, inplace=True)
            df_true_pred_labels.rename(columns={"entity": "true_entity"}, inplace=True)

            iter_idx = -1

            while comm_split <= num_entities:
                _,edge_betweenness = gtc.betweenness(G_gt)
                
                try:
                    edge = gtu.find_edge_range(G_gt, edge_betweenness, [sorted(edge_betweenness)[-5],max(edge_betweenness)])
                except:
                    edge = gtu.find_edge(G_gt, edge_betweenness, max(edge_betweenness))
                
                for e in edge:
                    G_gt.remove_edge(e)
                    split+=1

                G = gt2nx(G_gt, vp_graph)
                total_comp = nx.number_connected_components(G)
                
                if total_comp >= n:
                    iter_idx += 1
                    comm_split+=1
                    print("The graph has now {} components after removing edges.".format(nx.number_connected_components(G)))
                    print("The graph has broken after {} edge removals".format(split))
                    # break
                    # new_label_prop_comm = nx_comm.label_propagation_communities(G)
                    # new_communities = [list(c) for c in new_label_prop_comm]
                    # new_mod = nx_comm.modularity(G, new_communities)

                    communities = label_prop(G_gt,20)
                    new_communities = len(set(communities.fa))  # total number of communities
                    new_mod = gti.modularity(G_gt,communities)
                    print('new_mod: ', new_mod)

                    # get labels of the addresses
                    # predicted_entity_labels, df_pred = get_address_labels(G, df_local_gt, iter_idx)
                    count_of_known_entites, df_pred = get_address_labels(G, df_true_pred_labels, iter_idx)
                    print('df_true_pred_labels.shape, df_pred.shape: ', df_true_pred_labels.shape, df_pred.shape)
                    df_true_pred_labels = pd.merge(df_true_pred_labels, df_pred, left_on = "address", right_on = "address")
                    df_true_pred_labels.to_csv(dir_generated_files + 'comp_'+ str(subgraph_index) +'_true_pred_labels.csv',index=False)

                    # count_of_known_entites = len([value for key,value in predicted_entity_labels.items() if value!="Unknown"])
                    
                    # metrics
                    if iter_idx == 0:
                        labels_true, labels_pred = df_true_pred_labels['true_entity'], df_true_pred_labels['pred_entity_'+str(iter_idx)]
                    else:
                        labels_true, labels_pred = df_true_pred_labels['pred_entity_'+str(iter_idx-1)], df_true_pred_labels['pred_entity_'+str(iter_idx)]
                    ami = adjusted_mutual_info_score(labels_true=labels_true, labels_pred=labels_pred)
                    urs = rand_score(labels_true=labels_true, labels_pred=labels_pred)
                    homog = homogeneity_score(labels_true=labels_true, labels_pred=labels_pred)
                    (tn, fp), (fn, tp) = pair_confusion_matrix(labels_true, labels_pred)
                    tp = tp.astype(np.float64)
                    tn = tn.astype(np.float64)
                    fp = fp.astype(np.float64)
                    fn = fn.astype(np.float64)
                    if fn == 0 and fp == 0: ars = 1.0
                    else:
                        ars = 2. * (tp*tn - fn*fp) / ((tp+fn)*(fn+tn) + (tp+fp)*(fp+tn))

                    print('ami, ars, urs, homog: ', ami, ars, urs, homog)
                    modularity_list.append({
                                            'iter_idx': iter_idx,
                                            'total edge splits' : split, 
                                            'total component splits' : comm_split, 
                                            'number_of_components' : nx.number_connected_components(G),
                                            'number_of_communities': new_communities, 
                                            'new_modularity' : new_mod, 
                                            'original_modularity' : mod, 
                                            "count_of_known_entites" : count_of_known_entites,
                                            'subgraph_index': subgraph_index,
                                            'num_of_unique_entities_in_comp' : num_entities,
                                            'total_num_of_addresses_in_comp' : df_true_pred_labels.shape[0],
                                            "ami" : ami,
                                            "ars" : ars,
                                            "urs" : urs,
                                            "homog" : homog
                                        })
                    n = nx.number_connected_components(G)+1
                    G_gt, vp_graph = nx2gt(G)

                    # #compare separated components with the ground truth and verify that they split into same entity comps # #
            
            if num_entities == -1: continue

            ### graphs to be plotted after exiting the while loop ###
            # modularity change vs component splits
            # AMI, ARI, homogeneity change vs component splits
            # number of communities vs component split
            # graph showing the change in increasing address validation

            modularity_df = pd.DataFrame(modularity_list)
            modularity_df.to_csv(dir_generated_files + 'comp_'+ str(subgraph_index) +'_modularity.csv',index=False)

            plot_girvan_newmann_metrics(
                                            modularity_df['iter_idx'], 
                                            modularity_df['new_modularity'], 
                                            "Iterations \n ({} graph)".format(wt.capitalize()), 
                                            'Modularity', 
                                            'Girvin Newmann Modularity Mapping \n File idx: {}, Component idx: {} \n Original modularity: {}'.format(idx, modularity_df['subgraph_index'][0], round(modularity_df['original_modularity'][0], 4)),
                                            'blue', 
                                            fig_dir + 'comp_'+ str(subgraph_index) +'_modularity.png'
                                        )
            plot_girvan_newmann_metrics(
                                            modularity_df['iter_idx'], 
                                            modularity_df['count_of_known_entites'], 
                                            "Iterations \n ({} graph)".format(wt.capitalize()), 
                                            'count of addresses with known entities', 
                                            'Girvin Newmann count of known entites Mapping \n File idx: {}, Component idx: {} \n Num of unique entities: {} \n Total num of addresses: {}'.format(idx, modularity_df['subgraph_index'][0], modularity_df['num_of_unique_entities_in_comp'][0], modularity_df['total_num_of_addresses_in_comp'][0]),
                                            'red', 
                                            fig_dir + 'comp_'+ str(subgraph_index) +'_count_of_known_entites.png'
                                        )
            plot_girvan_newmann_metrics(
                                            modularity_df['total edge splits'].index, 
                                            modularity_df['number_of_communities'], 
                                            "Total edge splits \n ({} graph)".format(wt.capitalize()), 
                                            'Number of communities in the graph', 
                                            'The total communites generated with edge splits in the graph',                             
                                            'blue', 
                                            fig_dir + 'comp_'+ str(subgraph_index) +'_edge_splits_vs_communites.png'
                                        )

            metric_names = ['ami', 'ars', 'urs', 'homog']
            colurs = ['green', 'green2', 'yellow_80', 'turquoise']
            for j in range(len(metric_names)):
                plot_girvan_newmann_metrics(
                                                modularity_df['iter_idx'], 
                                                modularity_df[metric_names[j]], 
                                                "Iterations \n ({} graph)".format(wt.capitalize()), 
                                                metric_names[j].upper(), 
                                                'File idx: {}, Component idx: {}'.format(idx, modularity_df['subgraph_index'][0]),
                                                colurs[j], 
                                                fig_dir + 'comp_'+ str(subgraph_index) + metric_names[j] + '.png'
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

            # local data path (comment server path below when using local path)
            data_path = '../data/' # data path on local
            data_dir = data_path + cur + '/' + cur
            graph_data_dir = data_path + cur + '/' + cur

            # # server data path (comment local path above when using server path)
            # data_path = '/local/scratch/correspondence_network/Girvin_Newmann_data/btc_2012_logs/' # data path on server
            # data_dir = data_path + cur + '_logs/' + wt + '/' + heuristic + '/generated_files/' + cur
            # graph_data_dir = data_path + cur + '_logs/' + wt + '/' + heuristic + '/generated_files/graph/' + cur

            main(i, cur, heuristic, wt, PATHNAMES, data_dir, graph_data_dir, dir_generated_files, fig_dir)


