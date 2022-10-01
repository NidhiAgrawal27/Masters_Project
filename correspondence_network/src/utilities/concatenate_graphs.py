import numpy as np
import pandas as pd


def concat_addrs_data(df1, df2):
    
    df2['correct_address_id'] = np.nan

    for idx, row in df1.iterrows():
        addrs = row[0]
        id = row[1]

        if addrs in list(df2['address']): # Address is in both df1 and df2

            # assign id of 'addrs' from df1 to correct_address_id of 'addrs' in df2
            df2.loc[df2['address'] == addrs, 'correct_address_id'] = id

        else: # Address that are in df1 but not in df2 are concatenated to df2
            
            df2 = pd.concat([df2, df1[df1['address'] == addrs]])
            df2.loc[df2['address'] == addrs, 'correct_address_id'] = id

    df2.reset_index(drop=True, inplace=True)
    df2 = df2.convert_dtypes()

    # Assign correct_address_id to remaining addresses in df2
    idx_list = list(set(df2.index) - set(df2['correct_address_id'])) # remaining idx values that haven't been used as ids
    df2.loc[df2['correct_address_id'].isna(), 'correct_address_id'] = idx_list

    return df2



def change_node_ids(df_edge, df_addrs):

    node_list = []

    for idx, row in df_edge.iterrows():
        
        node1 = int(row[0])
        node2 = int(row[1])

        for node in [node1, node2]:

            if node not in node_list:
                
                new_node = df_addrs.loc[df_addrs['address_id'] == node, 'correct_address_id']
                
                # if there are more than one row with same previous address_id, then select the one where 
                # previous address id is not same as the correct_address_id
                # this is because edge data of df2 does not have the nodes from df1 that were initially not present in df2

                if len(new_node) > 1:
                    new_node = df_addrs.loc[(df_addrs['address_id'] == node) & 
                                                            (df_addrs['address_id'] != df_addrs['correct_address_id'])]
                    df_edge.loc[df_edge['node1'] == node, 'correct_node1'] = int(new_node['correct_address_id'])
                    df_edge.loc[df_edge['node2'] == node, 'correct_node2'] = int(new_node['correct_address_id'])
                else:
                    df_edge.loc[df_edge['node1'] == node, 'correct_node1'] = int(new_node)
                    df_edge.loc[df_edge['node2'] == node, 'correct_node2'] = int(new_node)
                
                node_list.append(node)

    return df_edge



def concat_edge_data(df_edge, df_edge_new_node_ids):
    
    df_stacked = pd.concat([df_edge, df_edge_new_node_ids], axis=0)
    df_stacked.reset_index(drop=True, inplace=True)
    df = df_stacked.groupby(['node1', 'node2'], as_index=False)[list(set(df_stacked.columns) - set(['node1', 'node2']))].sum()
    df.loc[df['h0'] > 0 , 'h0'] = 1
    if 'h1' in list(df.columns):
        df.loc[df['h1'] > 0 , 'h1'] = 1

    return df



def concat_addrs_edge(df_addrs_1, df_addrs_2, df_edge_1, df_edge_2):

    # step 1: concat both address dataframes and get new ids for nodes
    df_addrs_concat = concat_addrs_data(df_addrs_1, df_addrs_2)

    # step 2: get correct ids for node1 and node2 in edge data of second dataframe
    df_edge_2['correct_node1'] = df_edge_2['node1']
    df_edge_2['correct_node2'] = df_edge_2['node2']
    df_edge_new_node_ids = change_node_ids(df_edge_2, df_addrs_concat)
    
    # step 3: rename columns of above edge data of second dataframe
    df_edge_new_node_ids.drop(['node1', 'node2'], axis = 1, inplace=True)
    df_edge_new_node_ids.rename(columns={'correct_node1' : 'node1', 'correct_node2' : 'node2'}, inplace=True)

    # step 4: concatenate edge data of both dataframes
    df_edge_concat = concat_edge_data(df_edge_1, df_edge_new_node_ids)

    # step 5: rename columns of concatenated address dataframe from step 1
    df_addrs_concat.drop(['address_id'], axis = 1, inplace=True)
    df_addrs_concat.rename(columns={'correct_address_id' : 'address_id'}, inplace=True)

    return df_addrs_concat, df_edge_concat



def create_graph(graph, df_addrs_concat, df_edge_concat):

    for node in df_addrs_concat['address_id'] :
        vertex = graph.add_vertex()

    for idx, row in df_edge_concat.iterrows():
        v0 = row[0]
        v1 = row[1]
        e = graph.add_edge(v0,v1)
        
    return graph

