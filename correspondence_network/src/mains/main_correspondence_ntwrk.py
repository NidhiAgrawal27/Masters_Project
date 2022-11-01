import pandas as pd
import argparse
import pathlib
import os
import graph_tool as gt
from graph_tool import inference as gti
import graph_tool.topology as gtt
from graph_tool import draw
import tqdm as tqdm
from utilities import set_seed, compute_components, pathnames, correspondence_network
from utilities.modularity import get_entities
from utilities.visualization import plotPowerLaw, plot_density_graph

import warnings
warnings.filterwarnings('ignore')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    parser.add_argument("--currency", type=str, help="currency name example - btc: Bitcoin, iota: IoTa", required=True)
    parser.add_argument("--heuristic", type=str, help="name of heuristic, example: h0, or h0+h1", required=True)
    parser.add_argument("--vis", type=str, help="visualization: yes or no", required=True)
    parser.add_argument("--data_is_split", type=str, help="Data is read in chunks: yes or no", required=True)
    parser.add_argument("--save_graph", type=str, help="Save graph: yes or no", required=True)
    parser.add_argument("--load_graph", type=str, help="Load saved graph: yes or no", required=True)
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

    PATHNAMES = pathnames.pathnames(cur, heuristic)
    pathlib.Path(PATHNAMES['generated_files']).mkdir(parents=True, exist_ok=True)
    pathlib.Path(PATHNAMES['figure_dir']).mkdir(parents=True, exist_ok=True)
    dir_generated_files = PATHNAMES['generated_files'] + cur + '_' + heuristic + '_'
    fig_dir = PATHNAMES['figure_dir'] + cur + '_' + heuristic + '_'
    graph_path = dir_generated_files + 'graph.xml.gz'

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
                graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter)


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
                graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter)


        # start of no_modin_split
        elif data_is_split == 'no_modin_split':
            if cur == 'feathercoin' or cur == 'monacoin':
                chunks_df = pd.read_csv(PATHNAMES['data_path'], chunksize=chunksize,header=None)
                chunks_df.columns=['transaction_id','block_index','input_addresses_x','input_amounts_x',
                                        'output_addresses_y','output_amounts_y','timestamp']
            else: chunks_df = pd.read_csv(PATHNAMES['data_path'], chunksize=chunksize)            
            for i, df in enumerate(chunks_df):
                    graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter)
        # end of no_modin split

        print('\n\n' + cur + ' ' + heuristic + ': correspondence network created')

        # write csv file for transaction_ids
        if os.path.isfile(dir_generated_files + 'transaction_ids.csv') == False:
            df_tx_ids.to_csv(dir_generated_files + 'transaction_ids.csv', index=False)
            print(cur + ' ' + heuristic + ': writing transaction_ids.csv completed')
        else: print(cur + ' ' + heuristic + ': transaction_ids.csv exists')

        # save graph_of_correspondences
        if save_graph == 'yes':
            print(cur + ' ' + heuristic + ': saving graph...')
            graph_of_correspondences.save(dir_generated_files + 'graph.xml.gz')
            print(cur + ' ' + heuristic + ': graph saved')

    # load graph
    else:
        print('\n\nLoading graph: ', graph_path, '\n')
        print(cur + ' ' + heuristic + ': loading graph...')
        graph_of_correspondences = gt.load_graph(graph_path)
        print(cur + ' ' + heuristic + ': graph loaded')


    # compute components    
    components, _ = gtt.label_components(graph_of_correspondences)
    components_list = compute_components.compute_components(graph_of_correspondences, components)
    df_components = pd.DataFrame.from_dict(components_list, orient='columns')

    # compute modularity    
    get_entities(graph_of_correspondences, components, cur, heuristic, fig_dir)


    # map vertext and edge properties and write csv files for address_id
    if os.path.isfile(dir_generated_files + 'address_ids.csv') == False:
        for i in range(graph_of_correspondences.num_vertices()):
            vertices_mapping.append({'address' : graph_of_correspondences.vertex_properties[str(i)][i], 'address_id' : i})
        df_address_ids = pd.DataFrame.from_dict(vertices_mapping, orient='columns')
        df_address_ids.to_csv(dir_generated_files + 'address_ids.csv', index=False)
        print(cur + ' ' + heuristic + ': writing address_ids.csv completed')
    else: print(cur + ' ' + heuristic + ': address_ids.csv exists')

    # map vertext and edge properties and write csv files for edge data
    if os.path.isfile(dir_generated_files + 'edge_data.csv') == False:
        for e in graph_of_correspondences.edges(): 
            edge_mapping.append(graph_of_correspondences.edge_properties[str(e)][e])
        df_edge_data = pd.DataFrame.from_dict(edge_mapping, orient='columns')
        df_edge_data.to_csv(dir_generated_files + 'edge_data.csv', index=False)
        print(cur + ' ' + heuristic + ': writing edge_data.csv completed')
    else: print(cur + ' ' + heuristic + ': edge_data.csv exists')

    # map vertext and edge properties and write csv files for components data
    if os.path.isfile(dir_generated_files + 'components.csv') == False:    
        df_components.to_csv(dir_generated_files + 'components.csv', index=False)
        print(cur + ' ' + heuristic + ': writing components.csv completed')
    else: print(cur + ' ' + heuristic + ': components.csv exists')

    # visualization: density graph
    plot_density_graph(df_components['num_of_addrs'], 'Number of addesses', fig_dir + 'density_plot.png', cur, heuristic)
    print(cur + ' ' + heuristic + ': density_plot.png completed\n')

    # visualization: power law plot
    plotPowerLaw(df_components['num_of_addrs'], cur, heuristic, fig_dir + 'powerlaw_plot.png')
    print('\n'+ cur + ' ' + heuristic + ': powerlaw_plot.png completed')

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


