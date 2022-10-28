from utilities import add_nodes_edges, preprocessing


def correspondence_network(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter):
        
    preprocess = preprocessing.PreProcessing(df)

    col_to_drop = [x for x in df.columns[df.columns.str.contains('Unnamed')]] # for bitcoin data

    preprocess.drop_unnecessary_cols(cur, col_to_drop)
    
    preprocess.remove_nan_values(addrs_col = ['input_addresses_x', 'output_addresses_y'], 
                                amt_col = ['input_amounts_x', 'output_amounts_y'])

    df_tx_ids = preprocess.unique_tx_id_for_split_data(df_tx_ids)

    print(cur + ' ' + heuristic + ' iteration ' + str(iter) + ': Transaction ids created.')

    # create correspondence network
    preprocess.df.apply(
                add_nodes_edges.add_correspondence_single_edge_property, 
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

    iter += 1

    return graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter

def correspondence_network_directed(df, graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, cur, heuristic, iter):
        
    preprocess = preprocessing.PreProcessing(df)

    col_to_drop = [x for x in df.columns[df.columns.str.contains('Unnamed')]] # for bitcoin data

    preprocess.drop_unnecessary_cols(cur, col_to_drop)
    
    preprocess.remove_nan_values(addrs_col = ['input_addresses_x', 'output_addresses_y'], 
                                amt_col = ['input_amounts_x', 'output_amounts_y'])

    df_tx_ids = preprocess.unique_tx_id_for_split_data(df_tx_ids)

    print(cur + ' ' + heuristic + ' iteration ' + str(iter) + ': Transaction ids created.')

    # create correspondence network
    preprocess.df.apply(
                add_nodes_edges.add_correspondence_directed, 
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

    iter += 1

    return graph_of_correspondences, vertex_property, edge_property, nodes_dict, df_tx_ids, iter

