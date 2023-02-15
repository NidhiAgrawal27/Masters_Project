import networkx as nx
import pandas as pd

def get_address_labels(nx_graph, df_local_gt, iter_idx):
    df_pred = pd.DataFrame(columns=['address', 'pred_entity_'+str(iter_idx)])
    entity = {}
    nx.set_node_attributes(nx_graph, entity, "entity")
    # for comp in nx.connected_component_subgraph(nx_graph):
    for c in nx.connected_components(nx_graph):
        comp = nx_graph.subgraph(c)
        df_addrs = pd.DataFrame([vertex for vertex in comp.nodes()], columns = ["address"])
        df_merged = pd.merge(df_addrs,df_local_gt[['address', 'true_entity']],left_on="address",right_on="address", how = "outer")
        entities_list = list(df_merged['true_entity'])
        if 'Unknown' in entities_list: entities_list.remove('Unknown')
        count_of_known_entites = len(set(entities_list))
        new_rows_list = []
        if count_of_known_entites == 1:
            for nodename in comp.nodes():
                # entity[nodename] = entities_list[0]
                new_rows_list.append({'address':nodename, 'pred_entity_'+str(iter_idx):entities_list[0]})
        else:
            for nodename in comp.nodes():
                if iter_idx == 0:
                    new_rows_list.append({
                                            'address':nodename, 
                                            'pred_entity_'+str(iter_idx) : df_local_gt[df_local_gt['address']==nodename]['true_entity'].values[0], 
                                            'pred_entity_'+str(iter_idx)+'_unkown':'Unknown'
                                        })
                else:
                    new_rows_list.append({
                                            'address':nodename, 
                                            'pred_entity_'+str(iter_idx) : df_local_gt[df_local_gt['address']==nodename]['pred_entity_'+str(iter_idx-1)].values[0], 
                                            'address':nodename, 'pred_entity_'+str(iter_idx)+'_unkown':'Unknown'
                                        })
        for new_row in new_rows_list:        
            df_pred = df_pred.append(new_row, ignore_index=True)
    print('df_local_gt.shape, df_pred.shape: ', df_local_gt.shape, df_pred.shape)
    return count_of_known_entites, df_pred

