import pandas as pd
import numpy as np
import argparse
import pathlib
import os
import pickle
import graph_tool as gt
from graph_tool import inference as gti
import graph_tool.topology as gtt
from graph_tool import draw
import tqdm as tqdm
from utilities import set_seed, compute_components, pathnames, correspondence_network
from utilities.modularity import compute_modularity
from utilities.visualization import plotPowerLaw, plot_density_graph, plot_modularity_graph

import warnings
warnings.filterwarnings('ignore')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    parser.add_argument("--currency", type=str, help="currency name example - btc: Bitcoin, iota: IoTa", required=True)
    parser.add_argument("--heuristic", type=str, help="name of heuristic, example: h0, or h0_h1", required=True)
    parser.add_argument("--vis", type=str, help="visualization: yes or no", required=True)
    parser.add_argument("--data_is_split", type=str, help="Data is read in chunks: yes or no", required=True)
    parser.add_argument("--save_graph", type=str, help="Save graph: yes or no", required=True)
    parser.add_argument("--load_graph", type=str, help="Load saved graph: yes or no", required=True)
    parser.add_argument("--weighted", type=str, help="Weighted graph: yes or no", required=True)
    parser.add_argument("--chunksize", type=int, help="Chunk of data to be read in one iteration", required=False)

    args = parser.parse_args()

    set_seed.set_seed(args.seed)
    cur = args.currency
    heuristic = args.heuristic
    vis = args.vis
    chunksize = args.chunksize
    data_is_split = args.data_is_split
    save_graph = args.save_graph
    load_graph = args.load_graph
    weighted = args.weighted

    PATHNAMES = pathnames.pathnames(cur, heuristic, weighted)
    pathlib.Path(PATHNAMES['generated_files']).mkdir(parents=True, exist_ok=True)
    pathlib.Path(PATHNAMES['figure_dir']).mkdir(parents=True, exist_ok=True)
    dir_generated_files = PATHNAMES['generated_files'] + cur + '_' + heuristic + '_'
    fig_dir = PATHNAMES['figure_dir'] + cur + '_' + heuristic + '_'
    graph_dir = PATHNAMES['generated_files'] + 'graph/'
    pathlib.Path(graph_dir).mkdir(parents=True, exist_ok=True)
    graph_path = graph_dir + cur + '_' + heuristic + '_'
    if weighted == 'yes':
        dir_generated_files = dir_generated_files + 'wt_'
        fig_dir = fig_dir + 'wt_'
        graph_path = graph_path + 'wt_'
    

    graph_of_correspondences = gt.Graph( directed=False )
    vertex_property = graph_of_correspondences.new_vertex_property("string")
    edge_property = graph_of_correspondences.new_edge_property("object")
    nodes_dict = {}
    vertices_mapping = []
    edge_mapping = []
    df_tx_ids = pd.DataFrame()
    df_address_ids = pd.DataFrame()
    df_edge_data = pd.DataFrame()
    df_components = pd.DataFrame()
    iter = 0

    print('\n\n*********************** Processing of ' + cur + ' ' + heuristic + ' initiated ***********************\n')


    if load_graph == 'no':
        
        print()
        if data_is_split == 'no':
            if cur=='feathercoin' or cur=='monacoin':
                df = pd.read_csv(PATHNAMES['data_path'], header=None)
                df.columns=['transaction_id','block_index','input_addresses_x','input_amounts_x',
                                'output_addresses_y','output_amounts_y','timestamp']
            elif cur == 'btc_2012':
                df = pd.read_csv(PATHNAMES['data_path'], nrows=15000000)
                df_timestamp = pd.DataFrame(df['timestamp'].between(1310000000, 1360000000))
                idx = df_timestamp.index[df_timestamp['timestamp'] == True].tolist()
                df = df.iloc[idx]
            else: df = pd.read_csv(PATHNAMES['data_path'])

            print('Create Correspondence Network Progress Bar:')
            for i in tqdm.tqdm(range(1)):
                graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter, weighted)


        elif data_is_split == 'yes':
            import ray
            import modin.pandas as mpd
            ray.init()
            if cur == 'feathercoin' or cur == 'monacoin':
                chunks_df = mpd.read_csv(PATHNAMES['data_path'], chunksize=chunksize,header=None)
                chunks_df.columns=['transaction_id','block_index','input_addresses_x','input_amounts_x',
                                        'output_addresses_y','output_amounts_y','timestamp']
            else: chunks_df = mpd.read_csv(PATHNAMES['data_path'], chunksize=chunksize)
            iter = 0
            for df in chunks_df:
                df = df._to_pandas()
                graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter, weighted)


        # start of no_modin_split
        elif data_is_split == 'no_modin_split':
            if cur == 'feathercoin' or cur == 'monacoin':
                chunks_df = pd.read_csv(PATHNAMES['data_path'], chunksize=chunksize,header=None)
                chunks_df.columns=['transaction_id','block_index','input_addresses_x','input_amounts_x',
                                        'output_addresses_y','output_amounts_y','timestamp']
            else: chunks_df = pd.read_csv(PATHNAMES['data_path'], chunksize=chunksize)            
            for i, df in enumerate(chunks_df):
                    graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter, weighted)
        # end of no_modin split

        print('\n\n' + cur + ' ' + heuristic + ': correspondence network created')

        # write csv file for transaction_ids
        if os.path.isfile(dir_generated_files + 'transaction_ids.csv') == False:
            df_tx_ids.to_csv(dir_generated_files + 'transaction_ids.csv', index=False)
            print(cur + ' ' + heuristic + ': writing transaction_ids.csv completed')
        else: print(cur + ' ' + heuristic + ': transaction_ids.csv exists')

        # save graph_of_correspondences, address data and edge data
        if save_graph == 'yes':
            print(cur + ' ' + heuristic + ': saving graph and properties...')
            graph_of_correspondences.save(graph_path + 'graph.xml.gz')
            with open(graph_path + 'vertex_prop.pickle', 'wb') as handle:
                pickle.dump(vertex_property, handle, protocol=pickle.HIGHEST_PROTOCOL)
            with open(graph_path + 'edge_prop.pickle', 'wb') as handle:
                pickle.dump(edge_property, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print(cur + ' ' + heuristic + ': graph and properties saved')

             # map vertext and edge properties and write csv files for address_id
            for i in range(graph_of_correspondences.num_vertices()):
                vertices_mapping.append({'address' : vertex_property[i], 'address_id' : i})
            df_address_ids = pd.DataFrame.from_dict(vertices_mapping, orient='columns')
            df_address_ids.to_csv(dir_generated_files + 'address_ids.csv', index=False)
            print(cur + ' ' + heuristic + ': writing address_ids.csv completed')

            # map vertext and edge properties and write csv files for edge data
            for e in graph_of_correspondences.edges(): 
                edge_mapping.append(edge_property[e])
            df_edge_data = pd.DataFrame.from_dict(edge_mapping, orient='columns')
            df_edge_data.to_csv(dir_generated_files + 'edge_data.csv', index=False)
            print(cur + ' ' + heuristic + ': writing edge_data.csv completed')
            

    # load graph
    else:
        try:
            print('\n\nLoading graph: ' + graph_path + 'graph.xml.gz\n')
            print(cur + ' ' + heuristic + ': loading graph and properties...')
            graph_of_correspondences = gt.load_graph(graph_path + 'graph.xml.gz')
            with open(graph_path + 'vertex_prop.pickle', 'rb') as handle:
                vertex_property = pickle.load(handle)
            with open(graph_path + 'edge_prop.pickle', 'rb') as handle:
                edge_property = pickle.load(handle)
            print(cur + ' ' + heuristic + ': graph and properties loaded')
        except:
            print('ERROR: Load Graph failed. Graph not found on given path.')
            return

    # compute components    
    components, _ = gtt.label_components(graph_of_correspondences)
    components_list = compute_components.compute_components(graph_of_correspondences, components)
    df_components = pd.DataFrame.from_dict(components_list, orient='columns')

    # visualization: density graph
    plot_density_graph(df_components['num_of_addrs'], 'Number of addesses', fig_dir + 'density_plot.png', cur, heuristic)
    print(cur + ' ' + heuristic + ': density_plot.png completed\n')

    # visualization: power law plot
    plotPowerLaw(df_components['num_of_addrs'], cur, heuristic, fig_dir + 'powerlaw_plot.png')
    print('\n'+ cur + ' ' + heuristic + ': powerlaw_plot.png completed')

    # compute modularity, num of edges and num of communities in the components    
    comp_size, sz_comp_edges, sz_comp_comm, sz_comp_mod, entities = compute_modularity(graph_of_correspondences, components, heuristic)
    
    df_components["component_size"] = comp_size
    df_components["num_of_edges"] = sz_comp_edges

    if heuristic=="h0":
        df_components["num_of_communities"] = sz_comp_comm
        df_components["modularity"] = sz_comp_mod
        #save entities as a vertex property
        with open(graph_path + 'graph_vp_lp_entities.pickle', 'wb') as handle:
                pickle.dump(entities, handle, protocol=pickle.HIGHEST_PROTOCOL)
        #modularity of whole graph
        modularity = gti.modularity(graph_of_correspondences,entities)

    # map vertext and edge properties and write csv files for components data
    df_components.to_csv(dir_generated_files + 'components.csv', index=False)
    print(cur + ' ' + heuristic + ': writing components.csv completed')

    #title of the plots
    title = cur.capitalize() + ' ' + heuristic

    #visualisation: Component size vs Edges
    plot_modularity_graph(df_components, "num_of_edges", title, fig_dir + 'comp_size_edges.png')
    print(cur + ' ' + heuristic + ': comp_size_edges.png completed\n')

    if heuristic=="h0":
        #visualisation: Component size vs Number of communities
        plot_modularity_graph(df_components, "num_of_communities", title, fig_dir + 'comp_size_communities.png')
        print(cur + ' ' + heuristic + ': comp_size_communities.png completed\n')

        #visualisation: Component size vs Modularity
        plot_modularity_graph(df_components, "modularity", 'Modularity of ' + title + ' graph: ' + str(round(modularity, 4)), fig_dir + 'comp_size_modularity.png')
        print(cur + ' ' + heuristic + ': comp_size_modularity.png completed\n')

    # visualize network
    if vis == 'yes':
        if os.path.isfile(fig_dir + 'correspondence_network' + '.pdf') == False:
            draw.graph_draw(graph_of_correspondences, vertex_text=graph_of_correspondences.vertex_index, 
                            output = fig_dir + 'correspondence_network' + '.pdf')
            print(cur + ' ' + heuristic + ': network figure completed')
        else: print(cur + ' ' + heuristic + ': correspondence_network.pdf exists')

    print('\n\n*********************** Processing of ' + cur + ' ' + heuristic + ' completed ***********************\n')

    print()

if __name__ == "__main__":
    main()


