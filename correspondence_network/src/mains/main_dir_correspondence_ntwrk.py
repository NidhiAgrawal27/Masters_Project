import pandas as pd
import numpy as np
import argparse
import pathlib
import graph_tool as gt
from graph_tool import draw
from utilities import set_seed, compute_components, pathnames, correspondence_network
from utilities.visualization import plotPowerLaw, plot_density_graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    parser.add_argument("--currency", type=str, help="currency name example - btc: Bitcoin, iota: IoTa", required=True)
    parser.add_argument("--heuristic", type=str, help="name of heuristic, example: h0, or h0+h1", required=True)
    parser.add_argument("--vis", type=str, help="visualization: yes or no", required=True)
    parser.add_argument("--data_is_split", type=str, help="Data is read in chunks: yes or no", required=True)
    parser.add_argument("--chunksize", type=int, help="Chunk of data to be read in one iteration", required=False)

    args = parser.parse_args()

    set_seed.set_seed(args.seed)
    cur = args.currency
    heuristic = args.heuristic
    vis = args.vis
    chunksize = args.chunksize
    data_is_split = args.data_is_split

    PATHNAMES = pathnames.pathnames(cur, heuristic)
    pathlib.Path(PATHNAMES['generated_files']).mkdir(parents=True, exist_ok=True)
    pathlib.Path(PATHNAMES['figure_dir']).mkdir(parents=True, exist_ok=True)

    graph_of_correspondences = gt.Graph()
    nodes_dict = {}
    vertex_property = graph_of_correspondences.new_vertex_property("string")
    edge_property = graph_of_correspondences.new_edge_property("object")
    df_tx_ids = pd.DataFrame()
    iter = 0

    print('*********************** Processing of ' + cur + ' initiated ***********************\n')
    
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

        graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network_directed(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter)


    elif data_is_split == 'yes':

        #import ray
        import modin.pandas as mpd
        #ray.init()

        if cur == 'feathercoin' or cur == 'monacoin':
            chunks_df = mpd.read_csv(PATHNAMES['data_path'], chunksize=chunksize,header=None)
            chunks_df.columns=['transaction_id','block_index','input_addresses_x','input_amounts_x',
                                    'output_addresses_y','output_amounts_y','timestamp']

        else: chunks_df = mpd.read_csv(PATHNAMES['data_path'], chunksize=chunksize)

        iter = 0

        for df in chunks_df:
            df = df._to_pandas()
            graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network_directed(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter)
    

    # start of no_modin_split
    elif data_is_split == 'no_modin_split':
        # import ray
        # import modin.pandas as mpd
        # ray.init()
        if cur == 'feathercoin' or cur == 'monacoin':
            chunks_df = pd.read_csv(PATHNAMES['data_path'], chunksize=chunksize,header=None)
            chunks_df.columns=['transaction_id','block_index','input_addresses_x','input_amounts_x',
                                    'output_addresses_y','output_amounts_y','timestamp']
        else: chunks_df = pd.read_csv(PATHNAMES['data_path'], chunksize=chunksize)
        for df in chunks_df:
            # df = df._to_pandas()
            graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter = correspondence_network.correspondence_network_directed(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter)
    # end of no_modin split


    components = compute_components.compute_components(graph_of_correspondences)

    print(cur + ' ' + heuristic + ': correspondence network created.')
    print('\n')

    # Create df for address_id, edge and components data
    vertices_mapping = []
    for i in range(graph_of_correspondences.num_vertices()):
        vertices_mapping.append({'address' : vertex_property[i], 'address_id' : i})

    # edge_mapping = []
    # for e in graph_of_correspondences.edges(): 
    #     edge_mapping.append(edge_property[e])

    df_address_ids = pd.DataFrame.from_dict(vertices_mapping, orient='columns')
    # df_edge_data = pd.DataFrame.from_dict(edge_mapping, orient='columns')
    df_components = pd.DataFrame.from_dict(components, orient='columns')

    # visualization: density graph and power law plot
    fig_dir = PATHNAMES['figure_dir'] + cur + '_' + heuristic + '_'

    # Applying the Majority Voter State Model:
    state = compute_components.get_majority_voter_state(graph_of_correspondences,10,fig_dir + 'majority_voter.png')
    df_mvstates = pd.DataFrame.from_dict(state, orient='columns')

    plot_density_graph(df_components['num_of_addrs'], 'Number of addesses', fig_dir + 'density_plot.png', cur)

    # an array of degrees of all nodes in the graph
    degreeArray = np.asarray([d for d in graph_of_correspondences.degree_property_map('out').get_array()])
    avgDeg = np.mean(degreeArray)
    degSpacing = np.linspace(min(degreeArray),max(degreeArray),len(degreeArray)) # evenly spaced degrees

    # plot power-law probability distribution of the network
    plotPowerLaw(degreeArray, degSpacing, avgDeg, fig_dir + 'powerlaw_plot.png', cur)


    # write csv files for transaction_ids, address_id, edge and components data
    df_tx_ids.to_csv(PATHNAMES['generated_files'] + 'transaction_ids.csv', index=False)
    df_address_ids.to_csv(PATHNAMES['generated_files'] + 'address_ids.csv', index=False)
    # df_edge_data.to_csv(PATHNAMES['generated_files'] + 'edge_data.csv', index=False)
    df_components.to_csv(PATHNAMES['generated_files'] + 'components.csv', index=False)
    df_mvstates.to_csv(PATHNAMES['generated_files'] + 'mvstates.csv', index=False)
    print(cur + ' ' + heuristic + ': writing files completed.')

    # visualize network
    if vis == 'yes':
        draw.graph_draw(graph_of_correspondences, vertex_text=graph_of_correspondences.vertex_index, 
                        output = fig_dir + 'correspondence_network' + '.pdf')
        print(cur + ' ' + heuristic + ': network figure completed.')

    print('*********************** Processing of ' + cur + ' completed ***********************\n\n')


if __name__ == "__main__":
    main()


