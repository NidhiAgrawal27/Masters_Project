from utilities import add_nodes_edges, preprocessing
from tqdm import tqdm
tqdm.pandas()

def correspondence_network(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter):
    preprocess = preprocessing.PreProcessing(df)
    col_to_drop = [x for x in df.columns[df.columns.str.contains('Unnamed')]] # for bitcoin data
    preprocess.drop_unnecessary_cols(cur, col_to_drop)    
    preprocess.remove_nan_values(addrs_col = ['input_addresses_x', 'output_addresses_y'], 
                                amt_col = ['input_amounts_x', 'output_amounts_y'])
    df_tx_ids = preprocess.unique_tx_id_for_split_data(df_tx_ids)
    if cur == 'iota':
        for col in preprocess.df.columns:
            preprocess.df = preprocess.df[preprocess.df[col] != 'Not found']
    # create correspondence network
    print(cur + ' ' + heuristic + ' iter ' + str(iter) + ' Progress Bar:')
    preprocess.df.progress_apply(
                            add_nodes_edges.add_correspondence, 
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
    iter += 1
    return graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter

