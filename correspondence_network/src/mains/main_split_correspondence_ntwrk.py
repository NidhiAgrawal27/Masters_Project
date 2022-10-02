import modin.pandas as mpd
import pandas as pd
#import ray
import argparse
import pathlib
import graph_tool as gt
from graph_tool import draw
from utilities import utils, preprocessing, correspondence_network
from utilities.concatenate_graphs import concat_addrs_edge, create_graph


def main():

    #ray.init()

    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, help="random seed", required=True)
    parser.add_argument("--currency", type=str, help="currency name example - btc: Bitcoin, iota: IoTa", required=True)
    parser.add_argument("--heuristic", type=str, help="name of heuristic, example: h0, or h0+h1", required=True)
    parser.add_argument("--vis", type=str, help="visualization: yes or no", required=True)
    parser.add_argument("--chunksize", type=str, help="number of rows to be read at a time", required=True)

    args = parser.parse_args()

    utils.set_seed(args.seed)
    cur = args.currency
    heuristic = args.heuristic
    vis = args.vis
    chunksize = int(args.chunksize)
    data_is_split = 1

    PATHNAMES = utils.pathnames(cur, heuristic, data_is_split)
    dir_name = "../logs/" + 'split/' + cur + "_logs/" + heuristic + '/'
    PATHNAMES["figure_dir"] = dir_name + "figures/"
    PATHNAMES["generated_files"] = dir_name + "generated_files/"


    # Cleaning and preprocessing the data
    
    df_dict = {'df_addrs1': '', 'df_addrs2': '', 'df_edge1': '', 'df_edge1': ''}
    df_tx_ids = pd.DataFrame()
    iter = 0

    if cur == 'feathercoin' or cur == 'monacoin':
        chunks_df = mpd.read_csv(PATHNAMES['data_path'], chunksize=chunksize,header=None)
        chunks_df.columns=['transaction_id','block_index','input_addresses_x','input_amounts_x',
                                'output_addresses_y','output_amounts_y','timestamp']
    elif cur == 'btc_2011s': 
        df = mpd.read_csv(PATHNAMES['data_path'],nrows=15000000)
    else: chunks_df = mpd.read_csv(PATHNAMES['data_path'], chunksize=chunksize)
    

    for df in chunks_df:

        df = df._to_pandas()
        
        preprocess = preprocessing.PreProcessing(df)

        preprocess.drop_unnecessary_cols(cur)
        
        preprocess.remove_nan_values(addrs_col = ['input_addresses_x', 'output_addresses_y'], 
                                    amt_col = ['input_amounts_x', 'output_amounts_y'])

        pathlib.Path(PATHNAMES['generated_files']).mkdir(parents=True, exist_ok=True)
        df_tx_ids = preprocess.unique_tx_id_for_split_data(df_tx_ids)

        print(cur + ' ' + heuristic + ' iteration ' + str(iter) + ': preprocessing completed.')
        
        if iter == 0:
            # create correspondence network
            graph_of_correspondences = gt.Graph( directed=False )
            nodes_dict = {}
            vertex_property = graph_of_correspondences.new_vertex_property("string")
            edge_property = graph_of_correspondences.new_edge_property("object")

        # # create correspondence network
        # graph_of_correspondences = gt.Graph( directed=False )
        # nodes_dict = {}
        # vertex_property = graph_of_correspondences.new_vertex_property("string")
        # edge_property = graph_of_correspondences.new_edge_property("object")

        preprocess.df.apply(
                    correspondence_network.add_correspondence, 
                    graph_of_correspondences=graph_of_correspondences, 
                    ip_addrs_idx = 0, 
                    op_addrs_idx = 2, 
                    ip_amt_idx = 1, 
                    op_amt_idx = 3,
                    nodes_dict = nodes_dict,
                    vertex_property = vertex_property,
                    edge_property = edge_property,
                    heuristic = heuristic,
                    axis=1
                )

        print(cur + ' ' + heuristic + ' iteration ' + str(iter) + ' : correspondence network created.')
#         vertices_mapping = []
#         for i in range(graph_of_correspondences.num_vertices()):
#             vertices_mapping.append({'address' : vertex_property[i], 'address_id' : i})

#         edge_mapping = []
#         for e in graph_of_correspondences.edges(): 
#             edge_mapping.append(edge_property[e])

#         df_addrs = pd.DataFrame.from_dict(vertices_mapping, orient='columns')
#         df_edge = pd.DataFrame.from_dict(edge_mapping, orient='columns')

        iter += 1

#         if iter == 1:
#             df_dict['df_addrs1'] = df_addrs
#             df_dict['df_edge1'] = df_edge
#             continue
        
#         df_dict['df_addrs2'] = df_addrs
#         df_dict['df_edge2'] = df_edge

        # concatenate address and edge data of the current chunk with previous chunks

        # df_addrs_concat, df_edge_concat = concat_addrs_edge(df_dict['df_addrs1'], df_dict['df_addrs2'], 
        #                                                         df_dict['df_edge1'], df_dict['df_edge2'])
        # df_dict['df_addrs1'] = df_addrs_concat
        # df_dict['df_edge1'] = df_edge_concat


        

    # end of for loop for processing chunks

    # write csv files for address_id, edge and components data

#     df_dict['df_addrs1'].to_csv(PATHNAMES['generated_files'] + 'address_ids.csv', index=False)
#     df_dict['df_edge1'].to_csv(PATHNAMES['generated_files'] + 'edge_data.csv', index=False)
#     df_tx_ids.to_csv(PATHNAMES['generated_files'] + 'transaction_ids.csv', index=False)
    
#     graph = gt.Graph( directed=False )
#     create_graph(graph, df_dict['df_addrs1'], df_dict['df_edge1'])

#     components = correspondence_network.compute_components(graph)
#     df = pd.DataFrame.from_dict(components, orient='columns')
#     df.to_csv(PATHNAMES['generated_files'] + 'components.csv', index=False)

    components = correspondence_network.compute_components(graph_of_correspondences)

    print(cur + ' ' + heuristic + ': components computed.')

    # write csv files for address_id, edge and components data
    vertices_mapping = []
    for i in range(graph_of_correspondences.num_vertices()):
        vertices_mapping.append({'address' : vertex_property[i], 'address_id' : i})

    edge_mapping = []
    for e in graph_of_correspondences.edges(): 
        edge_mapping.append(edge_property[e])

    df = pd.DataFrame.from_dict(vertices_mapping, orient='columns')
    df.to_csv(PATHNAMES['generated_files'] + 'address_ids.csv', index=False)

    df = pd.DataFrame.from_dict(edge_mapping, orient='columns')
    df.to_csv(PATHNAMES['generated_files'] + 'edge_data.csv', index=False)
        
    df = pd.DataFrame.from_dict(components, orient='columns')
    df.to_csv(PATHNAMES['generated_files'] + 'components.csv', index=False)

    print(cur + ' ' + heuristic + ': writing files completed.')

    if vis == 'yes':

        fig_dir = PATHNAMES['figure_dir']
        pathlib.Path(fig_dir).mkdir(parents=True, exist_ok=True)
        draw.graph_draw(graph, vertex_text=graph.vertex_index, output = fig_dir + 'correspondence_network' + '.pdf')

        print(cur + ' ' + heuristic + ': figure completed.')



if __name__ == "__main__":
    main()

